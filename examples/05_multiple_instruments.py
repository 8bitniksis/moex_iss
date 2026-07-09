from moex_iss import ISSClient

SECURITIES = [
    "SBER",
    "GAZP",
    "LKOH"
]



def main():

    client = ISSClient()


    data = {}


    for sec in SECURITIES:

        print(
            f"Loading {sec}"
        )


        data[sec] = (
            client.candles_df(
                sec,
                interval=60
            )
        )


    for sec, df in data.items():

        print(
            sec,
            len(df)
        )


if __name__ == "__main__":
    main()