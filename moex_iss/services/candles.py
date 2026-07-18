from __future__ import annotations

import pandas as pd

from ..dataframe import ISSDataFrame
from .base import BaseService


class CandleService(BaseService):
    """Candlestick data service."""

    def raw(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
    ) -> dict:

        url = self._client.endpoint.candles(
            engine=engine,
            market=market,
            board=board,
            security=security,
            params={
                "interval": interval,
            },
        )

        return self._client.get_json(url)

    def df(
        self,
        security: str,
        engine: str = "stock",
        market: str = "shares",
        board: str = "TQBR",
        interval: int = 24,
    ) -> pd.DataFrame:

        raw = self.raw(
            security=security,
            engine=engine,
            market=market,
            board=board,
            interval=interval,
        )

        return ISSDataFrame.candles(raw)