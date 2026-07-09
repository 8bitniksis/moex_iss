import json

import pandas as pd
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)


from .config import ISSConfig
from .session import ISSSession
from .auth import ISSAuthenticator
from .endpoints import EndpointBuilder
from .pagination import ISSPaginator
from .dataframe import ISSDataFrame



class ISSClient:


    def __init__(
        self,
        config: ISSConfig | None = None
    ):

        self.config = (
            config
            or ISSConfig()
        )


        self.session = ISSSession(
            self.config
        )


        self.auth = ISSAuthenticator(
            self.session,
            self.config
        )


        if self.config.authenticated:

            self.auth.authenticate()


        self.endpoint = EndpointBuilder(
            self.config.base_url
        )


        self.paginator = ISSPaginator(
            self
        )



    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=10
        )
    )
    def get_json(
        self,
        url
    ):

        response = (
            self.session.get(url)
        )


        if response.status_code >= 500:

            raise RuntimeError(
                response.text
            )


        response.raise_for_status()


        return response.json()



    def get(
        self,
        path,
        params=None
    ):

        url = (
            self.endpoint.build(
                path,
                params
            )
        )


        return self.get_json(url)



    def iter_history(
        self,
        engine,
        market,
        board,
        security,
        from_date=None,
        till_date=None
    ):


        params = {}


        if from_date:
            params["from"] = from_date


        if till_date:
            params["till"] = till_date



        url = (
            self.endpoint.history_security(
                engine,
                market,
                board,
                security,
                params
            )
        )


        return self.paginator.iterate(
            url,
            "history"
        )



    def candles(
        self,
        security,
        engine="stock",
        market="shares",
        board="TQBR",
        interval=24
    ):


        url = (
            self.endpoint.candles(
                engine,
                market,
                board,
                security,
                {
                    "interval":interval
                }
            )
        )


        return self.get_json(url)
    
    def candles_df(
        self,
        security,
        engine="stock",
        market="shares",
        board="TQBR",
        interval=60
    ):


        raw = self.candles(
            security,
            engine,
            market,
            board,
            interval
        )


        return ISSDataFrame.candles(
            raw
        )
    
    def history_df(
        self,
        engine,
        market,
        board,
        security,
        from_date=None,
        till_date=None
    ):


        rows = list(
            self.iter_history(
                engine,
                market,
                board,
                security,
                from_date,
                till_date
            )
        )


        return pd.DataFrame(
            rows
        )