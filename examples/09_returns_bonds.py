from moex_iss import ISSClient


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

    snapshot = client.services.bonds.snapshot_df("RU000A10AHU1")

    print(snapshot)


if __name__ == "__main__":
    main()