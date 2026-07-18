from __future__ import annotations

from collections.abc import Iterator

import pandas as pd

from .base import BaseService


class HistoryService(BaseService):
    """Historical market data service."""

    def iter(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        from_date: str | None = None,
        till_date: str | None = None,
    ) -> Iterator[dict]:

        params: dict[str, str] = {}

        if from_date:
            params["from"] = from_date

        if till_date:
            params["till"] = till_date

        url = self._client.endpoint.history_security(
            engine=engine,
            market=market,
            board=board,
            security=security,
            params=params,
        )

        return self._client.paginator.iterate(
            url,
            "history",
        )

    def df(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        from_date: str | None = None,
        till_date: str | None = None,
    ) -> pd.DataFrame:

        rows = list(
            self.iter(
                engine=engine,
                market=market,
                board=board,
                security=security,
                from_date=from_date,
                till_date=till_date,
            )
        )

        return pd.DataFrame(rows)