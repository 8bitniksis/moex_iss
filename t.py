from moex_iss import ISSClient


client = ISSClient()


candles = client.candles(
    security="SBER",
    interval=60
)


print(candles.keys())