import json, datetime, winsound, time
from binance.client import Client
with open("api_key_secret.json") as f:
    info = json.load(f)
    # print(info)

print("High-Low")

API_KEY = info["API_KEY"]
API_SECRET = info["API_SECRET"]
AVERAGE_OF = info["AVERAGE_OF"]
all_list_usdt = info["COINS_LIST"]
MULTIPLY = info["MULTIPLY"]
sound_freq = info["SOUND_FREQUENCY"]
sound_duration = info["SOUND_DURATION"]

client = Client(API_KEY, API_SECRET)
account = client.get_account()
balances = (account["balances"])
time_list = [info["TIME1M"],info["TIME3M"],info["TIME5M"],info["TIME15M"],info["TIME30M"],info["TIME1H"],info["TIME4H"]]



timings = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE,
            Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_1HOUR,
            Client.KLINE_INTERVAL_4HOUR]

def unix_to_datetime(t):
    return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M')

def volume_avrg_check(timings):
    coin_count = 0  # to count coins
    for coin in all_list_usdt:  # taking coin name
        coin_count += 1
        # print("=================future HIGH-LOW=================")
        # print("count: ",coin_count)
        # print("coin: ",coin)
        time_is = timings.split("_")[-1]
        # print("minut:", time_is)
        candles = client.futures_klines(symbol=coin + "USDT", interval=timings)
        average = 0
        middle = len(candles[-AVERAGE_OF:-2])
        for high_low in candles[-AVERAGE_OF:-2]:
            average += float(high_low[2])-float(high_low[3])
            # print(unix_to_datetime(str(high_low[0])), "----", "High", high_low[2], "Low", high_low[3], "High-Low", float(high_low[2])-float(high_low[3]))

        result = average/middle
        # print(f"average of last {AVERAGE_OF-2} candles:", result)
        # print(unix_to_datetime(str(candles[-2][0])), "last closed candle HIGH, LOW, HIGH-LOW is:", candles[-2][2], "-", candles[-2][3], "-", (float(candles[-2][2])-float(candles[-2][3])))  # volume of last closed candle
        if (MULTIPLY * result) <= (float(candles[-2][2])-float(candles[-2][3])):
            winsound.Beep(sound_freq, sound_duration)
            print("---High Low-------",coin, "--",time_is)

def run():
    for i in range(len(time_list)):
        if time_list[i] == 1:
            volume_avrg_check(timings[i])

while(not time.sleep(5)):
    run()

#      time         open         high       low         close        vol
# [1641372060000, '46398.62', '46438.43', '46398.62', '46426.82', '247.064', 1641372119999, '11468935.99435', 2082, '167.530', '7776773.99518', '0']