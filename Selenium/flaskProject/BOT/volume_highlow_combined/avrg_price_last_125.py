import json, datetime
import pprint

from binance.client import Client
with open("api_key_secret.json") as f:
    info = json.load(f)

API_KEY = info["API_KEY"]
API_SECRET = info["API_SECRET"]

client = Client(API_KEY, API_SECRET)
account = client.get_account()


def avrg_price_last_125_min(coin="DOGE", min=125):
    timings = Client.KLINE_INTERVAL_1MINUTE
    candles = client.futures_klines(symbol=coin + "USDT", interval=timings, limit=min+1)  # will take last 126 1 min info
    all_prices = 0
    total_min = len(candles)-1
    print(total_min)
    for price in candles[:-1]:
        all_prices += float(price[4])
    av_price = all_prices/total_min
    print(av_price)

avrg_price_last_125_min()



# avrg_price_last_125_min(coin=coin, min=125)


# average = 0
# middle = len(candles[-AVERAGE_OF:-2])
# for high_low in candles[-AVERAGE_OF:-2]:
#     average += float(high_low[2])-float(high_low[3])
#     # print(unix_to_datetime(str(high_low[0])), "----", "High", high_low[2], "Low", high_low[3], "High-Low", float(high_low[2])-float(high_low[3]))
#
# result = average/middle
# # print(f"average of last {AVERAGE_OF-2} candles:", result)
# # print(unix_to_datetime(str(candles[-2][0])), "last closed candle HIGH, LOW, HIGH-LOW is:", candles[-2][2], "-", candles[-2][3], "-", (float(candles[-2][2])-float(candles[-2][3])))  # volume of last closed candle
# if (MULTIPLY * result) <= (float(candles[-2][2])-float(candles[-2][3])):
#     winsound.Beep(sound_freq, sound_duration)
#     print("---High Low-------",coin, "--",time_is)
#
# def run():
#     for i in range(len(time_list)):
#         if time_list[i] == 1:
#             volume_avrg_check(timings[i])
#
# while(not time.sleep(5)):
#     run()

#      time         open         high       low         close        vol
# [1641372060000, '46398.62', '46438.43', '46398.62', '46426.82', '247.064', 1641372119999, '11468935.99435', 2082, '167.530', '7776773.99518', '0']