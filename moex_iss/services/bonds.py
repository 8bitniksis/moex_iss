from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from .base import BaseService


class BondsService(BaseService):
    """Service for working with MOEX bonds."""

    def raw(
        self,
        engine: str = "stock",
        market: str = "bonds",
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        url = self._client.endpoint.bonds(
            engine=engine,
            market=market,
            params=params,
        )

        return self._client.get_json(url)

    def df(
        self,
        engine: str = "stock",
        market: str = "bonds",
        params: dict[str, Any] | None = None,
    ) -> pd.DataFrame:

        raw = self.raw(
            engine=engine,
            market=market,
            params=params,
        )

        securities = raw["securities"]

        return pd.DataFrame(
            data=securities["data"],
            columns=securities["columns"],
        )

    def details(
        self,
        security: str,
        engine: str = "stock",
        market: str = "bonds",
    ) -> dict[str, Any]:

        url = self._client.endpoint.bond(
            security=security,
            engine=engine,
            market=market,
        )

        return self._client.get_json(url)

    def snapshot(
        self,
        security: str,
        engine: str = "stock",
        market: str = "bonds",
    ) -> dict[str, Any]:
        """
        Returns normalized bond snapshot.
        """

        raw = self.details(
            security=security,
            engine=engine,
            market=market,
        )

        def extract(block_name: str) -> dict[str, Any]:
            block = raw.get(block_name)

            if not block or not block.get("data"):
                return {}

            return dict(
                zip(
                    block["columns"],
                    block["data"][0],
                    strict=False,
                )
            )

        sec = extract("securities")
        md = extract("marketdata")
        yld = extract("marketdata_yields")

        snapshot = {
            # identification
            "SECID": sec.get("SECID"),
            "SHORTNAME": sec.get("SHORTNAME"),
            "SECNAME": sec.get("SECNAME"),
            "ISIN": sec.get("ISIN"),
            "REGNUMBER": sec.get("REGNUMBER"),

            # issue
            "BONDTYPE": sec.get("BONDTYPE"),
            "BONDSUBTYPE": sec.get("BONDSUBTYPE"),
            "LISTLEVEL": sec.get("LISTLEVEL"),

            # nominal
            "FACEVALUE": sec.get("FACEVALUE"),
            "FACEUNIT": sec.get("FACEUNIT"),
            "LOTSIZE": sec.get("LOTSIZE"),
            "LOTVALUE": sec.get("LOTVALUE"),
            "ISSUESIZE": sec.get("ISSUESIZE"),
            "ISSUESIZEPLACED": sec.get("ISSUESIZEPLACED"),

            # coupon
            "COUPONVALUE": sec.get("COUPONVALUE"),
            "COUPONPERCENT": sec.get("COUPONPERCENT"),
            "COUPONPERIOD": sec.get("COUPONPERIOD"),
            "NEXTCOUPON": sec.get("NEXTCOUPON"),
            "ACCRUEDINT": sec.get("ACCRUEDINT"),

            # dates
            "SETTLEDATE": sec.get("SETTLEDATE"),
            "MATDATE": sec.get("MATDATE"),
            "OFFERDATE": sec.get("OFFERDATE"),
            "BUYBACKDATE": sec.get("BUYBACKDATE"),

            # prices
            "LAST": md.get("LAST"),
            "BID": md.get("BID"),
            "OFFER": md.get("OFFER"),
            "WAPRICE": md.get("WAPRICE"),
            "PREVWAPRICE": sec.get("PREVWAPRICE"),

            # yields
            "YIELD": md.get("YIELD"),
            "YIELDATWAPRICE": md.get("YIELDATWAPRICE"),
            "EFFECTIVEYIELD": yld.get("EFFECTIVEYIELD"),

            # duration / spreads
            "DURATION": yld.get("DURATION"),
            "ZSPREADBP": yld.get("ZSPREADBP"),
            "GSPREADBP": yld.get("GSPREADBP"),

            # trading
            "NUMTRADES": md.get("NUMTRADES"),
            "VOLTODAY": md.get("VOLTODAY"),
            "VALTODAY": md.get("VALTODAY"),
            "TRADINGSTATUS": md.get("TRADINGSTATUS"),
        }

        # computed fields
        if snapshot["MATDATE"]:
            maturity = date.fromisoformat(snapshot["MATDATE"])
            snapshot["DAYSTOREDEMPTION"] = (maturity - date.today()).days
        else:
            snapshot["DAYSTOREDEMPTION"] = None

        if snapshot["NEXTCOUPON"]:
            next_coupon = date.fromisoformat(snapshot["NEXTCOUPON"])
            snapshot["COUPONDAYSREMAIN"] = (next_coupon - date.today()).days
        else:
            snapshot["COUPONDAYSREMAIN"] = None

        return snapshot