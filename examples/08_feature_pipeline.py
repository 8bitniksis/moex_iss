from moex_iss import ISSClient


def add_features(df):

    df["return"] = (
        df["close"]
        .pct_change()
    )


    df["volatility"] = (
        df["return"]
        .rolling(50)
        .std()
    )


    df["volume_zscore"] = (

        (
            df["volume"]
            -
            df["volume"].rolling(50).mean()
        )

        /

        df["volume"].rolling(50).std()

    )


    return df



def main():

    client = ISSClient()


    df = client.candles_df(
        "SiZ5",
        engine="futures",
        market="forts",
        board="RFUD",
        interval=10
    )


    df = add_features(df)


    print(
        df.tail()
    )


if __name__ == "__main__":
    main()