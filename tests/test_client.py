from moex_iss.endpoints import EndpointBuilder


def test_history_endpoint():


    builder = EndpointBuilder(
        "https://iss.moex.com"
    )


    url = builder.history_security(
        "stock",
        "shares",
        "TQBR",
        "SBER"
    )


    assert (
        "SBER"
        in url
    )


    assert (
        "history"
        in url
    )