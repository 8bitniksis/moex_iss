from moex_iss.dataframe import ISSDataFrame


def test_candle_dataframe(
    iss_candle_response
):

    df = ISSDataFrame.candles(
        iss_candle_response
    )


    assert df.index.name=="begin"


    assert df.iloc[0]["close"]==103