from moex_iss import ISSClient


def main():

    client = ISSClient()


    df = client.candles_df(
        security="GAZP",
        interval=60
    )


    print(df.tail())


    df.to_csv(
        "gazp_1h.csv"
    )


if __name__ == "__main__":
    main()