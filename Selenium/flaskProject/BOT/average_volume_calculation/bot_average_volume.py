import json, datetime, winsound, time, pprint
from binance.client import Client
with open("api_key_secret.json") as f:
    info = json.load(f)
    # print(info)



API_KEY = info["API_KEY"]
API_SECRET = info["API_SECRET"]

AVERAGE_OF = info["AVERAGE_OF"]
all_list_usdt = info["COINS_LIST"]
MULTIPLY = info["MULTIPLY"]
sound_freq = info["SOUND_FREQUENCY"]
sound_duration = info["SOUND_DURATION"]
EXTRA = info["EXTRA"]
client = Client(API_KEY, API_SECRET)
account = client.get_account()
balances = (account["balances"])
time_list = [info["TIME1M"],info["TIME3M"],info["TIME5M"],info["TIME15M"],info["TIME30M"],info["TIME1H"],info["TIME4H"]]



timings = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE,
            Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_1HOUR,
            Client.KLINE_INTERVAL_4HOUR]

pprint.pprint(client.get_historical_trades(symbol="DOGEUSDT"))

print(f"Av. Volume  and  High-Low, MULTIPLY={MULTIPLY}")
def unix_to_datetime(t):
    return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M')

def volume_avrg_check(timings):
    coin_count = 0  # to count coins
    for coin in all_list_usdt:  # taking coin name
        coin_count += 1
        # print("=================future volume=================")
        # print("count: ",coin_count)
        # print("coin: ",coin)
        time_is = timings.split("_")[-1]
        # print("minut:", time_is)
        candles = client.futures_klines(symbol=coin + "USDT", interval=timings)
        # print(candles)
        average_vol = 0
        average_high_low = 0
        middle = len(candles[-AVERAGE_OF:-3])
        for vol_hl in candles[-AVERAGE_OF:-3]:
            # print(unix_to_datetime(str(volume[0])), "----", volume[5])
            average_vol += float(vol_hl[5])  # volume
            print(float(vol_hl[2])-float(vol_hl[3]))
            average_high_low += float(vol_hl[2])-float(vol_hl[3])  # high low

        if average_vol != 0 and average_high_low !=0:
            avrg_result_vol = average_vol/middle
            last_closed_vol = float(candles[-2][5])  # last closed volume

            avrg_result_hl = average_high_low/middle
            last_closed_hl = float(candles[-2][2])-float(candles[-2][3])  # last closed high - low


            try:
                if (avrg_result_vol*MULTIPLY) <= last_closed_vol:  # checking volume
                    level_vol = round(last_closed_vol/avrg_result_vol, 2)  # how high is last closed candle vol compare with avrg.
                    level_hl = round(last_closed_hl/avrg_result_hl, 2)  #

                    winsound.Beep(sound_freq, sound_duration)
                    print("-----------", coin, "-------- Volume level is: ",f"{level_vol}x",f"------ High-Low level is:  {level_hl}x ---- time:", time_is)
            except Exception as e:
                print(e, f"coin is {coin}, avrg vol is: {avrg_result_vol}, last vol is: {last_closed_vol}, avrg high-low is {avrg_result_hl}, "
                         f"last closed high-low is: {last_closed_hl}")
                print(candles[-AVERAGE_OF:-3])
                continue


def run():

    print()
    for i in range(len(time_list)):
        if time_list[i] == 1:
            volume_avrg_check(timings[i])


if __name__=="__main__":
    while(not time.sleep(5)):
        run()
        print("Next Round")
