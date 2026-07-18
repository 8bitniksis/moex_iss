from __future__ import annotations

from datetime import date
from typing import Any, cast

import pandas as pd

from moex_iss.services.base import BaseService


class BondService(BaseService):
    """Service for working with MOEX corporate and government bonds."""

    def raw(
        self,
        engine: str = "stock",
        market: str = "bonds",
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Return the raw MOEX ISS response containing
        the list of available bonds.
        """

        url = self._client.endpoint.bonds(
            engine=engine,
            market=market,
            params=params,
        )

        return cast(
            dict[str, Any],
            self._client.get_json(url),
        )

    def df(
        self,
        engine: str = "stock",
        market: str = "bonds",
        params: dict[str, Any] | None = None,
    ) -> pd.DataFrame:
        """
        Return the list of bonds as a pandas DataFrame.
        """

        raw = self.raw(
            engine=engine,
            market=market,
            params=params,
        )

        return self._dataframe(
            raw["securities"],
        )

    def details(
        self,
        security: str,
        engine: str = "stock",
        market: str = "bonds",
    ) -> dict[str, Any]:
        """
        Return the raw ISS response for a single bond.
        """

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
        Return a normalized bond snapshot.
        """

        raw = self.details(
            security=security,
            engine=engine,
            market=market,
        )

        description = self._security_description(
            security=security,
        )

        return self._build_snapshot(
            raw=raw,
            description=description,
        )

    def snapshot_df(
        self,
        security: str,
        engine: str = "stock",
        market: str = "bonds",
    ) -> pd.DataFrame:
        """
        Return a normalized bond snapshot
        as a pandas DataFrame.
        """

        snapshot = self.snapshot(
            security=security,
            engine=engine,
            market=market,
        )

        return pd.DataFrame([snapshot])

    def _build_snapshot(
        self,
        raw: dict[str, Any],
        description: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build a normalized bond snapshot from
        ISS response blocks.
        """

        sec = self._table(raw, "securities")
        md = self._table(raw, "marketdata")
        yld = self._table(raw, "marketdata_yields")

        snapshot = {
            # Identification
            "SECID": sec.get("SECID"),
            "SHORTNAME": sec.get("SHORTNAME"),
            "SECNAME": sec.get("SECNAME"),
            "ISIN": sec.get("ISIN"),
            "REGNUMBER": sec.get("REGNUMBER"),
            # Bond classification
            "BONDTYPE": sec.get("BONDTYPE"),
            "BONDSUBTYPE": sec.get("BONDSUBTYPE"),
            "LISTLEVEL": sec.get("LISTLEVEL"),
            # Issue
            "FACEVALUE": sec.get("FACEVALUE"),
            "FACEUNIT": sec.get("FACEUNIT"),
            "LOTSIZE": sec.get("LOTSIZE"),
            "LOTVALUE": sec.get("LOTVALUE"),
            "ISSUESIZE": sec.get("ISSUESIZE"),
            "ISSUESIZEPLACED": sec.get("ISSUESIZEPLACED"),
            # Coupon
            "COUPONVALUE": sec.get("COUPONVALUE"),
            "COUPONPERCENT": sec.get("COUPONPERCENT"),
            "COUPONPERIOD": sec.get("COUPONPERIOD"),
            "NEXTCOUPON": sec.get("NEXTCOUPON"),
            "ACCRUEDINT": sec.get("ACCRUEDINT"),
            # Dates
            "SETTLEDATE": sec.get("SETTLEDATE"),
            "MATDATE": sec.get("MATDATE"),
            "OFFERDATE": sec.get("OFFERDATE"),
            "BUYBACKDATE": sec.get("BUYBACKDATE"),
            # Prices
            "LAST": md.get("LAST"),
            "BID": md.get("BID"),
            "OFFER": md.get("OFFER"),
            "WAPRICE": md.get("WAPRICE"),
            "PREVWAPRICE": sec.get("PREVWAPRICE"),
            # Yields
            "YIELD": md.get("YIELD"),
            "YIELDATWAPRICE": md.get("YIELDATWAPRICE"),
            "EFFECTIVEYIELD": yld.get("EFFECTIVEYIELD"),
            # Duration
            "DURATION": yld.get("DURATION"),
            # Credit spreads
            "ZSPREADBP": yld.get("ZSPREADBP"),
            "GSPREADBP": yld.get("GSPREADBP"),
            # Trading
            "NUMTRADES": md.get("NUMTRADES"),
            "VOLTODAY": md.get("VOLTODAY"),
            "VALTODAY": md.get("VALTODAY"),
            "TRADINGSTATUS": md.get("TRADINGSTATUS"),
        }

        snapshot.update(self._computed_fields(snapshot))

        snapshot.update(self._description_fields(description))

        return snapshot

    def _computed_fields(
        self,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Calculate derived bond metrics.
        """

        result: dict[str, Any] = {}

        matdate = snapshot.get("MATDATE")

        if matdate:
            maturity = date.fromisoformat(matdate)

            result["DAYSTOREDEMPTION"] = (maturity - date.today()).days
        else:
            result["DAYSTOREDEMPTION"] = None

        coupon = snapshot.get("NEXTCOUPON")

        if coupon:
            next_coupon = date.fromisoformat(coupon)

            result["COUPONDAYSREMAIN"] = (next_coupon - date.today()).days
        else:
            result["COUPONDAYSREMAIN"] = None

        return result

    def _description_fields(
        self,
        description: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Extract normalized fields from
        the ISS description block.
        """

        return {
            "NAME": description.get("NAME"),
            "TYPENAME": description.get("TYPENAME"),
            "EMITENTNAME": description.get("EMITENTNAME"),
            "INN": description.get("INN"),
            "PRIMARY_BOARDID": description.get("PRIMARY_BOARDID"),
            "PRIMARY_BOARD_TITLE": description.get("PRIMARY_BOARD_TITLE"),
            "IS_COLLATERAL": description.get("IS_COLLATERAL"),
            "IS_EXTERNAL": description.get("IS_EXTERNAL"),
            "IS_RII": description.get("IS_RII"),
            "EMITTER_ID": description.get("EMITTER_ID"),
            "INCLUDEDBYMOEX": description.get("INCLUDEDBYMOEX"),
            "IS_QUALIFIED_INVESTORS": description.get("IS_QUALIFIED_INVESTORS"),
            "HIGH_RISK": description.get("HIGH_RISK"),
            "COUPONFREQUENCY": description.get("COUPONFREQUENCY"),
            "EVENINGSESSION": description.get("EVENINGSESSION"),
            "MORNINGSESSION": description.get("MORNINGSESSION"),
            "WEEKENDSESSION": description.get("WEEKENDSESSION"),
            "SUSPENSION_LISTING": description.get("SUSPENSION_LISTING"),
            "ISSUEDATE": description.get("ISSUEDATE"),
            "INITIALFACEVALUE": description.get("INITIALFACEVALUE"),
            "SECSUBTYPE": description.get("SECSUBTYPE"),
            "STARTDATEMOEX": description.get("STARTDATEMOEX"),
            "REPLBOND": description.get("REPLBOND"),
            "ADMISSION_TYPE": description.get("ADMISSION_TYPE"),
        }
