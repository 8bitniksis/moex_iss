from urllib.parse import urlencode


class EndpointBuilder:

    def __init__(
        self,
        base_url: str
    ):
        self.base_url = base_url.rstrip("/")


    def build(
        self,
        path: str,
        params: dict | None = None
    ) -> str:

        url = (
            self.base_url
            + "/iss"
            + path
            + ".json"
        )

        if params:

            url += "?" + urlencode(params)

        return url



    def candles(
        self,
        engine: str,
        market: str,
        board: str,
        security: str,
        params=None
    ):

        path = (
            f"/history/engines/{engine}"
            f"/markets/{market}"
            f"/boards/{board}"
            f"/securities/{security}"
            f"/candles"
        )

        return self.build(
            path,
            params
        )



    def history_security(
        self,
        engine,
        market,
        board,
        security,
        params=None
    ):

        path = (
            f"/history/engines/{engine}"
            f"/markets/{market}"
            f"/boards/{board}"
            f"/securities/{security}"
        )

        return self.build(
            path,
            params
        )