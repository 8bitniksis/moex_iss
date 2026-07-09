from moex_iss.parser import parse_block


def test_parse_history(iss_history_response):

    block = parse_block("history", iss_history_response)

    rows = list(block.rows())

    assert len(rows) == 2

    assert rows[0]["SECID"] == "SBER"

    assert rows[0]["CLOSE"] == 250.5
