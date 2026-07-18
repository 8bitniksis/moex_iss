from moex_iss.clients.client import ISSClient
from moex_iss.dataframe.query import Query


def main():
    client = ISSClient()

    # Return dataFram of all bonds
    # df = client.services.bonds.df()
    # print(df.head())
    # print(df.columns)

    # Return individual bond by SECID
    # bond_details = client.services.bonds.details("RU000A10AHU1")
    # print(bond_details)

    # bond = client.services.bonds.snapshot("RU000A10AHU1")

    # print(bond["SHORTNAME"])
    # print(bond["MATDATE"])
    # print(bond["EFFECTIVEYIELD"])
    # print(bond["DURATION"])
    # print(bond["ZSPREADBP"])

    df = (
        client.services
            .bond
            .df()
    )
    
    result = (
        Query(df)
            .where("LISTLEVEL <= 2")
            .where("YIELD > 20")
            .where("DURATION < 365")
            .order_by_desc("YIELD")
            .take(30)
            .select("SECID", "SHORTNAME", "YIELD", "DURATION")
            .to_df()
    )

    print(result)


if __name__ == "__main__":
    main()