import pandas as pd

from .parser import parse_block


class ISSDataFrame:
    @staticmethod
    def from_block(payload: dict, block: str) -> pd.DataFrame:

        parsed = parse_block(block, payload)

        rows = list(parsed.rows())

        df = pd.DataFrame(rows)

        return df

    @staticmethod
    def candles(payload: dict) -> pd.DataFrame:

        df = ISSDataFrame.from_block(payload, "candles")

        if "begin" in df.columns:
            df["begin"] = pd.to_datetime(df["begin"])

            df = df.set_index("begin").sort_index()

        return df

    @staticmethod
    def history(payload: dict) -> pd.DataFrame:

        return ISSDataFrame.from_block(payload, "history")
