import pytest


@pytest.fixture
def iss_history_response():

    return {

        "history": {

            "metadata": {},

            "columns": [
                "TRADEDATE",
                "SECID",
                "CLOSE",
                "VOLUME"
            ],

            "data": [

                [
                    "2025-01-01",
                    "SBER",
                    250.5,
                    100000
                ],

                [
                    "2025-01-02",
                    "SBER",
                    252.0,
                    120000
                ]

            ]
        }
    }



@pytest.fixture
def iss_candle_response():

    return {

        "candles": {

            "columns":[
                "begin",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ],

            "data":[

                [
                    "2025-01-01 10:00:00",
                    100,
                    105,
                    99,
                    103,
                    5000
                ]

            ]
        }
    }