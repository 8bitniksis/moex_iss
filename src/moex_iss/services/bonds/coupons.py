from __future__ import annotations

from datetime import date
from typing import Any, cast

import pandas as pd

from moex_iss.services.base import BaseService


class BondCouponService(BaseService):
    """
    Service for working with bond cash flows.

    Provides access to coupon schedules,
    amortization schedules and combined
    cash flow data.
    """

    def raw(
        self,
        security: str,
    ) -> dict[str, Any]:
        """
        Return raw bondization response.
        """

        url = self._client.endpoint.bondization(
            security=security,
        )

        return cast(
                dict[str, Any],
                self._client.get_json(url),
            )

    def coupons(
        self,
        security: str,
    ) -> pd.DataFrame:
        """
        Return coupon schedule.
        """

        raw = self.raw(security)

        return self._block_to_dataframe(
            raw,
            "coupons",
        )

    def amortizations(
        self,
        security: str,
    ) -> pd.DataFrame:
        """
        Return amortization schedule.
        """

        raw = self.raw(security)

        return self._block_to_dataframe(
            raw,
            "amortizations",
        )

    def cashflow(
        self,
        security: str,
    ) -> pd.DataFrame:
        """
        Return complete cash flow
        ordered by payment date.
        """

        coupons = self.coupons(security)
        amortizations = self.amortizations(security)

        if not coupons.empty:
            coupons = coupons.copy()
            coupons["TYPE"] = "Coupon"

        if not amortizations.empty:
            amortizations = amortizations.copy()
            amortizations["TYPE"] = "Principal"

        frames = [
            df
            for df in (
                coupons,
                amortizations,
            )
            if not df.empty
        ]

        if not frames:
            return pd.DataFrame()

        return (
            pd.concat(
                frames,
                ignore_index=True,
            )
            .sort_values("DATE")
            .reset_index(drop=True)
        )

    def future_cashflow(
        self,
        security: str,
    ) -> pd.DataFrame:
        """
        Return future cash flows only.
        """

        df = self.cashflow(security)

        if df.empty:
            return df

        return df[
            pd.to_datetime(df["DATE"]).dt.date >= date.today()
        ].reset_index(drop=True)

    @staticmethod
    def _block_to_dataframe(
        raw: dict[str, Any],
        block: str,
    ) -> pd.DataFrame:
        """
        Convert ISS block into DataFrame.
        """

        data = raw.get(block)

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(
            data=data["data"],
            columns=data["columns"],
        )