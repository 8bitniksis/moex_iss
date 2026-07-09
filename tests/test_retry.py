import responses

from moex_iss import ISSClient


@responses.activate
def test_retry_on_server_error():


    url = (
        "https://iss.moex.com"
        "/iss/test.json"
    )


    responses.add(
        responses.GET,
        url,
        status=503
    )


    responses.add(
        responses.GET,
        url,
        status=503
    )


    responses.add(
        responses.GET,
        url,
        json={
            "ok":True
        },
        status=200
    )


    client=ISSClient()


    result=client.get_json(
        url
    )


    assert result["ok"] is True