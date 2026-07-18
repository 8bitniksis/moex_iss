from __future__ import annotations

import pandas as pd

from moex_iss.services.base import BaseService


class BondAnalyticsService(BaseService):
    """
    Analytics for bond DataFrames.

    All methods operate on already loaded
    pandas DataFrames and do not perform
    requests to MOEX ISS.
    """

    def average_yield(
        self,
        df: pd.DataFrame,
        column: str = "YIELD",
    ) -> float:
        """
        Return average bond yield.

        Parameters
        ----------
        df
            Bond DataFrame.
        column
            Yield column.

        Returns
        -------
        float
            Average yield.
        """

        return float(df[column].dropna().mean())

    def average_duration(
        self,
        df: pd.DataFrame,
        column: str = "DURATION",
    ) -> float:
        """
        Return average duration.

        Parameters
        ----------
        df
            Bond DataFrame.
        column
            Duration column.

        Returns
        -------
        float
            Average duration.
        """

        return float(df[column].dropna().mean())

    def ytm_curve(
        self,
        df: pd.DataFrame,
        duration_column: str = "DURATION",
        yield_column: str = "YIELD",
    ) -> pd.DataFrame:
        """
        Build Yield-To-Maturity curve.

        Returns
        -------
        pandas.DataFrame
            Duration / Yield pairs.
        """

        return (
            df[
                [
                    duration_column,
                    yield_column,
                ]
            ]
            .dropna()
            .sort_values(duration_column)
            .reset_index(drop=True)
        )

    def duration_distribution(
        self,
        df: pd.DataFrame,
        bins: int = 10,
        column: str = "DURATION",
    ) -> pd.DataFrame:
        """
        Build duration distribution.

        Returns
        -------
        pandas.DataFrame
            Bucket statistics.
        """

        distribution = (
            pd.cut(
                df[column],
                bins=bins,
            )
            .value_counts()
            .sort_index()
        )

        return distribution.rename("COUNT").rename_axis("BUCKET").reset_index()

    def maturity_distribution(
        self,
        df: pd.DataFrame,
        column: str = "MATDATE",
    ) -> pd.DataFrame:
        """
        Return maturity year distribution.
        """

        years = pd.to_datetime(df[column]).dt.year

        result = (
            years.value_counts()
            .sort_index()
            .rename("COUNT")
            .rename_axis("YEAR")
            .reset_index()
        )

        return result

    def coupon_distribution(
        self,
        df: pd.DataFrame,
        bins: int = 10,
        column: str = "COUPONPERCENT",
    ) -> pd.DataFrame:
        """
        Return coupon distribution.
        """

        distribution = (
            pd.cut(
                df[column],
                bins=bins,
            )
            .value_counts()
            .sort_index()
        )

        return distribution.rename("COUNT").rename_axis("BUCKET").reset_index()

    def liquidity_distribution(
        self,
        df: pd.DataFrame,
        bins: int = 10,
        column: str = "VALTODAY",
    ) -> pd.DataFrame:
        """
        Return liquidity distribution.
        """

        distribution = (
            pd.cut(
                df[column],
                bins=bins,
            )
            .value_counts()
            .sort_index()
        )

        return distribution.rename("COUNT").rename_axis("BUCKET").reset_index()
