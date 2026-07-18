from moex_iss.clients.client import ISSClient


def main():

    client = ISSClient()

    df = client.candles_df(
        security="SiZ5", engine="futures", market="forts", board="RFUD", interval=60
    )

    print(df.head())


if __name__ == "__main__":
    main()
