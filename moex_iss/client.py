import pandas as pd
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .auth import ISSAuthenticator
from .config import ISSConfig
from .dataframe import ISSDataFrame
from .endpoints import EndpointBuilder
from .exceptions import (
    ISSConnectionError,
    ISSRateLimitError,
    ISSResponseError,
    ISSServerError,
)
from .limiter import RateLimiter
from .pagination import ISSPaginator
from .session import ISSSession


class ISSClient:
    def __init__(self, config: ISSConfig | None = None, rate_limit=5):

        self.config = config or ISSConfig()

        self.limiter = RateLimiter(rate_limit)

        self.session = ISSSession(self.config)

        self.auth = ISSAuthenticator(self.session, self.config)

        if self.config.authenticated:
            self.auth.authenticate()

        self.endpoint = EndpointBuilder(self.config.base_url)

        self.paginator = ISSPaginator(self)

    @retry(
        retry=retry_if_exception_type((ISSServerError, ISSConnectionError)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    def get_json(self, url):

        self.limiter.wait()

        response = self.session.get(url)

        if 500 <= response.status_code < 600:
            raise ISSServerError(response.status_code, response.text)

        if response.status_code == 429:
            raise ISSRateLimitError("Too many requests")

        if response.status_code >= 400:
            raise ISSResponseError(response.status_code)

        response.raise_for_status()

        return response.json()

    def get(self, path, params=None):

        url = self.endpoint.build(path, params)

        return self.get_json(url)

    def iter_history(
        self, engine, market, board, security, from_date=None, till_date=None
    ):

        params = {}

        if from_date:
            params["from"] = from_date

        if till_date:
            params["till"] = till_date

        url = self.endpoint.history_security(engine, market, board, security, params)

        return self.paginator.iterate(url, "history")

    def candles(
        self, security, engine="stock", market="shares", board="TQBR", interval=24
    ):

        url = self.endpoint.candles(
            engine, market, board, security, {"interval": interval}
        )

        return self.get_json(url)

    def candles_df(
        self, security, engine="stock", market="shares", board="TQBR", interval=60
    ):

        raw = self.candles(security, engine, market, board, interval)

        return ISSDataFrame.candles(raw)

    def history_df(
        self, engine, market, board, security, from_date=None, till_date=None
    ):

        rows = list(
            self.iter_history(engine, market, board, security, from_date, till_date)
        )

        return pd.DataFrame(rows)
