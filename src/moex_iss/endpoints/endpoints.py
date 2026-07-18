from typing import Any
from urllib.parse import urlencode


class EndpointBuilder:
    def __init__(
        self,
        base_url: str,
    ) -> None:
        self.base_url = base_url.rstrip("/")

    def build(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> str:

        url = self.base_url + "/iss" + path + ".json"

        if params:
            url += "?" + urlencode(params)

        return url

    def candles(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        params: dict[str, Any] | None = None,
    ) -> str:

        path = (
            f"/engines/{engine}"
            f"/markets/{market}"
            f"/boards/{board}"
            f"/securities/{security}"
            f"/candles"
        )

        return self.build(path, params)

    def history_security(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        params: dict[str, Any] | None = None,
    ) -> str:

        path = (
            f"/history/engines/{engine}"
            f"/markets/{market}"
            f"/boards/{board}"
            f"/securities/{security}"
        )

        return self.build(path, params)

    def bonds(
        self,
        engine: str = "stock",
        market: str = "bonds",
        params: dict[str, Any] | None = None,
    ) -> str:
        path = f"/engines/{engine}/markets/{market}/securities"

        return self.build(path, params)

    def bond(
        self,
        security: str,
        engine: str = "stock",
        market: str = "bonds",
    ) -> str:

        path = f"/engines/{engine}/markets/{market}/securities/{security}"

        return self.build(path)

    def security(
        self,
        security: str,
        params: dict[str, Any] | None = None,
    ) -> str:
        path = f"/securities/{security}"

        return self.build(path, params)
