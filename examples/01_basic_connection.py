from moex_iss import ISSClient


def main():

    client = ISSClient()

    result = client.get("/engines")

    print(result.keys())


if __name__ == "__main__":
    main()
