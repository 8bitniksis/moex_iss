from moex_iss.dataframe import ISSDataFrame



def test_history_dataframe(
    iss_history_response
):


    df = ISSDataFrame.history(
        iss_history_response
    )


    assert len(df)==2


    assert (
        "CLOSE"
        in df.columns
    )


    assert (
        df.iloc[0]["SECID"]
        ==
        "SBER"
    )