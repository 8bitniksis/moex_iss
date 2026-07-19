from __future__ import annotations

from typing import Any

import pandas as pd

from moex_iss.dataframe import ISSDataFrame
from moex_iss.services.base import BaseService


class CandleService(BaseService):
    """Candlestick data service."""

    def raw(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
        from_date: str | None = None,
        till_date: str |None = None,
    ) -> dict[str, Any]:

        params: dict[str, Any] = {
            "interval": interval,
        }

        if from_date is not None:
            params["from"] = from_date

        if till_date is not None:
            params["till"] = till_date

        url = self._client.endpoint.candles(
            engine=engine,
            market=market,
            board=board,
            security=security,
            params=params,
        )

        return self._client.get_json(url)

    def df(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
        from_date: str | None = None,
        till_date: str | None = None,
    ) -> pd.DataFrame:

        raw = self.raw(
            security=security,
            engine=engine,
            market=market,
            board=board,
            interval=interval,
            from_date=from_date,
            till_date=till_date,
        )

        return ISSDataFrame.candles(raw)