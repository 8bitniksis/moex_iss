from pathlib import Path

from moex_iss.clients.client import ISSClient


def main():

    Path("data").mkdir(exist_ok=True)

    client = ISSClient()

    df = client.candles_df("SBER", interval=10)

    df.to_parquet("data/sber_10m.parquet")

    print("saved")


if __name__ == "__main__":
    main()
