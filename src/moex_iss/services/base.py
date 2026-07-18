from __future__ import annotations

from typing import Any

import pandas as pd


class BaseService:
    """Base class for all ISS services."""

    def __init__(
        self,
        client: Any,
    ) -> None:
        self._client = client

    def _table(
        self,
        raw: dict[str, Any],
        block_name: str,
    ) -> dict[str, Any]:
        """
        Convert an ISS table block into a dictionary.

        Parameters
        ----------
        raw
            Raw ISS response.
        block_name
            Name of the ISS response block.

        Returns
        -------
        dict[str, Any]
            Dictionary representing the first row of the block.
            Returns an empty dictionary if the block is missing
            or contains no rows.
        """

        block = raw.get(block_name)

        if not block:
            return {}

        data = block.get("data")

        if not data:
            return {}

        return dict(
            zip(
                block["columns"],
                data[0],
                strict=False,
            )
        )

    def _dataframe(
        self,
        block: dict[str, Any],
    ) -> pd.DataFrame:
        """
        Convert an ISS table block into a pandas DataFrame.
        """

        return pd.DataFrame(
            data=block["data"],
            columns=block["columns"],
        )

    def _security_description(
        self,
        security: str,
    ) -> dict[str, Any]:
        """
        Load and normalize the ISS security description.

        Parameters
        ----------
        security
            Security identifier.

        Returns
        -------
        dict[str, Any]
            Description fields indexed by field name.
        """

        url = self._client.endpoint.security(
            security=security,
            params={
                "iss.only": "description",
            },
        )

        raw = self._client.get_json(url)

        block = raw.get("description")

        if not block:
            return {}

        columns = block["columns"]

        result: dict[str, Any] = {}

        for row in block["data"]:
            values = dict(
                zip(
                    columns,
                    row,
                    strict=False,
                )
            )

            name = values.get("NAME") or values.get("name")
            value = values.get("VALUE") or values.get("value")

            if name is not None:
                result[name] = value

        return result
