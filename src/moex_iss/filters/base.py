from __future__ import annotations

from collections.abc import Callable

import pandas as pd


class BaseFilter:
    """Base class for DataFrame filters."""

    def __init__(self) -> None:
        self._filters: list[Callable[[pd.DataFrame], pd.Series]] = []

    def apply(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Apply all filters to a DataFrame.
        """

        if df.empty:
            return df

        mask = pd.Series(
            True,
            index=df.index,
        )

        for condition in self._filters:
            mask &= condition(df)

        return df.loc[mask].copy()