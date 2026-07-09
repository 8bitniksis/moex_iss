from moex_iss import ISSClient


def main():

    client = ISSClient()

    df = client.history_df(
        engine="stock",
        market="shares",
        board="TQBR",
        security="SBER",
        from_date="2025-01-01",
        till_date="2025-02-01",
    )

    print(df.head())

    print(df.describe())


if __name__ == "__main__":
    main()
