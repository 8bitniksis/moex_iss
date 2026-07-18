from collections.abc import Iterator
from typing import Any, cast

import pandas as pd
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from moex_iss.auth import ISSAuthenticator
from moex_iss.config import ISSConfig
from moex_iss.endpoints import EndpointBuilder
from moex_iss.services import ServiceContainer
from moex_iss.sessions.session import ISSSession
from moex_iss.utils.exceptions import (
    ISSConnectionError,
    ISSRateLimitError,
    ISSResponseError,
    ISSServerError,
)
from moex_iss.utils.limiter import RateLimiter
from moex_iss.utils.pagination import ISSPaginator


class ISSClient:
    """Main ISS client."""

    def __init__(
        self,
        config: ISSConfig | None = None,
        rate_limit: int = 5,
    ) -> None:

        self.config = config or ISSConfig()

        self.limiter = RateLimiter(rate_limit)

        self.session = ISSSession(self.config)

        self.auth = ISSAuthenticator(
            self.session,
            self.config,
        )

        if self.config.authenticated:
            self.auth.authenticate()

        self.endpoint = EndpointBuilder(
            self.config.base_url,
        )

        self.paginator = ISSPaginator(self)

        #
        # Services
        #
        self.services = ServiceContainer(self)

    @retry(
        retry=retry_if_exception_type(
            (
                ISSServerError,
                ISSConnectionError,
            )
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=10,
        ),
    )
    def get_json(
        self,
        url: str,
    ) -> dict[str, Any]:

        self.limiter.wait()

        response = self.session.get(url)

        if 500 <= response.status_code < 600:
            raise ISSServerError(
                response.status_code,
                response.text,
            )

        if response.status_code == 429:
            raise ISSRateLimitError(
                "Too many requests",
            )

        if response.status_code >= 400:
            raise ISSResponseError(
                response.status_code,
            )

        response.raise_for_status()

        return cast(
            dict[str, Any],
            response.json(),
        )

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        url = self.endpoint.build(
            path,
            params,
        )

        return self.get_json(url)

    #
    # ------------------------------------------------------------------
    # Backward compatible API
    # ------------------------------------------------------------------
    #

    def iter_history(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        from_date: str | None = None,
        till_date: str | None = None,
    ) -> Iterator[dict[str, Any]]:

        return self.services.history.iter(
            engine=engine,
            market=market,
            board=board,
            security=security,
            from_date=from_date,
            till_date=till_date,
        )

    def history_df(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        from_date: str | None = None,
        till_date: str | None = None,
    ) -> pd.DataFrame:

        return self.services.history.df(
            engine=engine,
            market=market,
            board=board,
            security=security,
            from_date=from_date,
            till_date=till_date,
        )

    def candles(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
    ) -> dict[str, Any]:

        return self.services.candles.raw(
            security=security,
            engine=engine,
            market=market,
            board=board,
            interval=interval,
        )

    def candles_df(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
    ) -> pd.DataFrame:

        return self.services.candles.df(
            security=security,
            engine=engine,
            market=market,
            board=board,
            interval=interval,
        )