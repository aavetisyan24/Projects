import json, datetime, winsound, time
from binance.client import Client
from datetime import datetime
with open("api_key_secret.json") as f:
    info = json.load(f)
    # print(info)

print("MA-100   MA-25")

API_KEY = info["API_KEY"]
API_SECRET = info["API_SECRET"]
MA_100 = info["MA_100"]
MA_25 = info["MA_25"]
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

def ma_100_ma25(timings):
    coin_count = 0  # to count coins
    for coin in all_list_usdt:  # taking coin name
        coin_count += 1
        # print("=================future MA100 - MA25=================")
        # print("count: ",coin_count)
        # print("coin: ",coin)
        time_is = timings.split("_")[-1]
        # print("minut:", time_is)
        candles = client.futures_klines(symbol=coin + "USDT", interval=timings, limit=1000)
        print(len(candles))
        MA_100_count = 0
        middle1 = len(candles[-MA_100:-2])
        for closed_price_ma100 in candles[-MA_100:-2]:
            MA_100_count += float(closed_price_ma100[4])
            # print(unix_to_datetime(str(closed_price_ma100[0])), "----", "Closed_price", closed_price_ma100[4])

        MA_25_count = 0
        middle2 = len(candles[-MA_25:-2])
        for closed_price_ma25 in candles[-MA_25:-2]:
            MA_25_count += float(closed_price_ma25[4])
            # print(unix_to_datetime(str(closed_price_ma25[0])), "----", "Closed_price", closed_price_ma25[4])



        result_100 = MA_100_count/middle1
        result_25 = MA_25_count/middle2

        # print(f"average of last {MA_100-2} candles closed price is: ", result_100)
        # print(f"average of last {MA_25-2} candles closed price is: ", result_25)

        # print("======================================================",result_25-((result_25*0.5)/100))

        if ((result_100 >= result_25) and result_100 < result_25+((result_25*MULTIPLY)/100)) or \
                ((result_100 < result_25) and result_100 > result_25-((result_25*MULTIPLY)/100)):
            winsound.Beep(sound_freq, sound_duration)
            print("--------", timings, "---------", coin)
            print(result_25, result_100)



def run():
    for i in range(len(time_list)):
        if time_list[i] == 1:
            ma_100_ma25(timings[i])
    print("Stopped for 5m", datetime.now().strftime("%H:%M:%S"))
    time.sleep(300)
    print("rounded", datetime.now().strftime("%H:%M:%S"))

while(not time.sleep(5)):
    print("Starting...", datetime.now().strftime("%H:%M:%S"))
    run()


#      time         open         high       low         close        vol
# [1641372060000, '46398.62', '46438.43', '46398.62', '46426.82', '247.064', 1641372119999, '11468935.99435', 2082, '167.530', '7776773.99518', '0']