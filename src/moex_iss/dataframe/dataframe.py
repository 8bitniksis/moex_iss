from typing import Any

import pandas as pd

from moex_iss.utils.parser import parse_block


class ISSDataFrame:
    @staticmethod
    def from_block(
        payload: dict[str, Any],
        block: str,
    ) -> pd.DataFrame:

        parsed = parse_block(block, payload)

        rows = list(parsed.rows())

        df = pd.DataFrame(rows)

        return df

    @staticmethod
    def candles(
        payload: dict[str, Any],
    ) -> pd.DataFrame:

        df = ISSDataFrame.from_block(payload, "candles")

        if "begin" in df.columns:
            df["begin"] = pd.to_datetime(df["begin"])

            df = df.set_index("begin").sort_index()

        return df

    @staticmethod
    def history(
        payload: dict[str, Any],
    ) -> pd.DataFrame:

        return ISSDataFrame.from_block(payload, "history")
