from moex_iss.clients.client import ISSClient


def main():

    client = ISSClient()

    result = client.get("/engines")

    print(result.keys())


if __name__ == "__main__":
    main()
