# moex_iss/dataframe/query.py
from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

import pandas as pd


class Query:
    """
    LINQ-style query engine for pandas DataFrame.

    Provides fluent API for filtering, sorting, grouping,
    and aggregating DataFrame data.

    Example:
        result = (
            Query(df)
                .where("YIELD > 18")
                .order_by_desc("YIELD")
                .take(20)
                .select("SECID", "SHORTNAME", "YIELD")
                .to_df()
        )
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initialize Query with a DataFrame.

        Args:
            dataframe: Source DataFrame (will be copied to avoid mutation)
        """
        self._df = dataframe.copy()

    # =========================================================================
    # Terminal Operations (возвращают результат, завершают цепочку)
    # =========================================================================

    def to_df(self) -> pd.DataFrame:
        """Return the resulting DataFrame."""
        return self._df.copy()

    def first(self) -> pd.Series:
        """
        Return the first row as a Series.

        Raises:
            ValueError: If DataFrame is empty
        """
        if self._df.empty:
            raise ValueError("Query result is empty, cannot get first row")
        return self._df.iloc[0]

    def first_or_none(self) -> pd.Series | None:
        """Return the first row as a Series, or None if empty."""
        if self._df.empty:
            return None
        return self._df.iloc[0]

    def single(self) -> pd.Series:
        """
        Return the single row as a Series.

        Raises:
            ValueError: If DataFrame is empty or has more than one row
        """
        if self._df.empty:
            raise ValueError("Query result is empty, cannot get single row")
        if len(self._df) > 1:
            raise ValueError(
                f"Query result has {len(self._df)} rows, expected exactly 1"
            )
        return self._df.iloc[0]

    # =========================================================================
    # Filtering
    # =========================================================================

    def where(
        self,
        condition: str | Callable[[pd.DataFrame], pd.Series],
    ) -> Query:
        """
        Filter rows by condition.

        Args:
            condition: SQL-like string or callable returning boolean mask

        Examples:
            .where("YIELD > 20")
            .where("PRICE > 90 and PRICE < 105")
            .where(lambda df: df["PRICE"] > 90)
        """
        if isinstance(condition, str):
            self._df = self._df.query(condition)
        else:
            mask = condition(self._df)
            self._df = self._df.loc[mask]
        return self

    # =========================================================================
    # Projection
    # =========================================================================

    def select(self, *columns: str) -> Query:
        """
        Select specific columns.

        Raises:
            KeyError: If any column doesn't exist
        """
        missing = [c for c in columns if c not in self._df.columns]
        if missing:
            raise KeyError(f"Columns not found: {missing}")
        self._df = self._df.loc[:, list(columns)]
        return self

    def drop(self, *columns: str) -> Query:
        """Drop specified columns."""
        self._df = self._df.drop(
            columns=[c for c in columns if c in self._df.columns]
        )
        return self

    def rename(self, **mapping: str) -> Query:
        """
        Rename columns.

        Example:
            .rename(PRICE="Price", YIELD="Yield")
        """
        self._df = self._df.rename(columns=mapping)
        return self

    def with_column(
        self,
        name: str,
        func: Callable[[pd.DataFrame], pd.Series],
    ) -> Query:
        """
        Add a new computed column.

        Example:
            .with_column("PRICE_RUB", lambda df: df["PRICE"] * 10)
        """
        self._df = self._df.copy()
        self._df[name] = func(self._df)
        return self

    # =========================================================================
    # Ordering
    # =========================================================================

    def order_by(
        self,
        column: str,
        ascending: bool = True,
    ) -> Query:
        """Sort by column ascending."""
        self._df = self._df.sort_values(column, ascending=ascending)
        return self

    def order_by_desc(self, column: str) -> Query:
        """Sort by column descending."""
        return self.order_by(column, ascending=False)

    def order_by_many(
        self,
        *columns: tuple[str, bool],
    ) -> Query:
        """
        Sort by multiple columns.

        Example:
            .order_by_many(("YIELD", False), ("DURATION", True))
        """
        cols = [c[0] for c in columns]
        ascending = [c[1] for c in columns]
        self._df = self._df.sort_values(cols, ascending=ascending)
        return self

    # =========================================================================
    # Pagination
    # =========================================================================

    def take(self, count: int) -> Query:
        """Take first N rows."""
        self._df = self._df.head(count)
        return self

    def skip(self, count: int) -> Query:
        """Skip first N rows."""
        self._df = self._df.iloc[count:]
        return self

    def page(self, page_number: int, page_size: int) -> Query:
        """
        Get specific page (1-indexed).

        Example:
            .page(2, 20)  # rows 21-40
        """
        start = (page_number - 1) * page_size
        self._df = self._df.iloc[start : start + page_size]
        return self

    # =========================================================================
    # Distinct
    # =========================================================================

    def distinct(self, *columns: str) -> Query:
        """
        Remove duplicate rows.

        If columns specified, deduplicate by those columns only.
        """
        if columns:
            self._df = self._df.drop_duplicates(subset=list(columns))
        else:
            self._df = self._df.drop_duplicates()
        return self

    # =========================================================================
    # Grouping
    # =========================================================================

    def group_by(self, *columns: str) -> GroupedQuery:
        """
        Group by columns. Returns GroupedQuery for aggregation.

        Example:
            .group_by("FACEUNIT").agg(avg_yield=("YIELD", "mean"))
        """
        return GroupedQuery(self._df, list(columns))

    # =========================================================================
    # Aggregation (terminal operations)
    # =========================================================================

    def count(self) -> int:
        """Return number of rows."""
        return len(self._df)

    def sum(self, column: str) -> Any:
        """Return sum of column."""
        return self._df[column].sum()

    def avg(self, column: str) -> Any:
        """Return mean of column."""
        return self._df[column].mean()

    def max(self, column: str) -> Any:
        """Return max of column."""
        return self._df[column].max()

    def min(self, column: str) -> Any:
        """Return min of column."""
        return self._df[column].min()

    # =========================================================================
    # Magic methods
    # =========================================================================

    def __len__(self) -> int:
        return len(self._df)

    def __repr__(self) -> str:
        return f"Query(rows={len(self._df)}, columns={list(self._df.columns)})"


class GroupedQuery:
    """
    Represents a grouped DataFrame for aggregation operations.
    """

    def __init__(self, dataframe: pd.DataFrame, group_columns: list[str]) -> None:
        self._df = dataframe
        self._group_columns = group_columns
        self._grouped = dataframe.groupby(group_columns)

    def agg(self, **kwargs: Any,) -> pd.DataFrame:
        """
        Aggregate with named operations.

        Example:
            .agg(
                avg_yield=("YIELD", "mean"),
                max_price=("PRICE", "max"),
                count=("SECID", "count"),
            )
        """
        result = self._grouped.agg(**kwargs).reset_index()
        return cast(pd.DataFrame, result)

    def count(self) -> pd.DataFrame:
        """Count rows in each group."""
        return self._grouped.size().reset_index(name="count")

    def sum(self, column: str) -> pd.DataFrame:
        """Sum column by group."""
        return self._grouped[column].sum().reset_index()

    def mean(self, column: str) -> pd.DataFrame:
        """Mean of column by group."""
        return self._grouped[column].mean().reset_index()
