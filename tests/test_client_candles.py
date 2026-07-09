import json
import responses


from moex_iss import ISSClient



@responses.activate
def test_candles_request():


    url = (
        "https://iss.moex.com"
        "/iss/history/engines/"
        "stock/markets/shares/"
        "boards/TQBR/"
        "securities/SBER/"
        "candles.json"
        "?interval=60"
    )


    with open(
        "tests/fixtures/candles.json"
    ) as f:

        payload=json.load(f)



    responses.add(
        responses.GET,
        url,
        json=payload,
        status=200
    )


    client=ISSClient()


    result = client.candles(
        "SBER",
        interval=60
    )


    assert (
        "candles"
        in result
    )


    assert (
        len(
            result["candles"]["data"]
        )
        ==
        1
    )