from pathlib import Path

from moex_iss.clients.client import ISSClient


def add_features(df):
    df["return"] = df["close"].pct_change()

    df["volatility"] = df["return"].rolling(50).std()

    df["volume_zscore"] = (
        df["volume"] - df["volume"].rolling(50).mean()
    ) / df["volume"].rolling(50).std()

    return df


def main():
    client = ISSClient()

    df = client.candles_df(
        "MMU6",
        engine="futures",
        market="forts",
        board="RFUD",
        interval=10,
        from_date="2026-06-25",
        till_date="2026-07-15",
    )

    df = add_features(df)

    # examples/data/
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_file = data_dir / "MMU6_10m_features.csv"

    df.to_csv(
        output_file,
        encoding="utf-8-sig",
        index=True,
    )

    print(f"Saved {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()