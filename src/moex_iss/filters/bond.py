from __future__ import annotations

from .base import BaseFilter


class BondFilter(BaseFilter):
    """Filter builder for bond DataFrames."""

    def secid(
        self,
        *secids: str,
    ) -> BondFilter:
        """
        Filter by security identifiers.
        """

        self._filters.append(lambda df: df["SECID"].isin(secids))

        return self

    def isin(
        self,
        *isins: str,
    ) -> BondFilter:
        """
        Filter by ISIN.
        """

        self._filters.append(lambda df: df["ISIN"].isin(isins))

        return self

    def list_level(
        self,
        *levels: int,
    ) -> BondFilter:
        """
        Filter by quotation list level.
        """

        self._filters.append(lambda df: df["LISTLEVEL"].isin(levels))

        return self

    def currency(
        self,
        *currencies: str,
    ) -> BondFilter:
        """
        Filter by face value currency.
        """

        self._filters.append(lambda df: df["FACEUNIT"].isin(currencies))

        return self
