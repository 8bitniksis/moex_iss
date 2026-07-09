import responses

from moex_iss import ISSClient


@responses.activate
def test_client_get_json():

    url = "https://iss.moex.com/iss/test.json"

    responses.add(responses.GET, url, json={"test": "ok"}, status=200)

    client = ISSClient()

    result = client.session.get(url).json()

    assert result["test"] == "ok"
