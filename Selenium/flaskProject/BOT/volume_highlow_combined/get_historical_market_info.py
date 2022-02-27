import json, datetime, winsound, time
import pprint

from binance.client import Client
with open("api_key_secret.json") as f:
    info = json.load(f)
    # print(info)



API_KEY = info["API_KEY"]
API_SECRET = info["API_SECRET"]
AVERAGE_OF = info["AVERAGE_OF"]
all_list_usdt = info["COINS_LIST"]
MULTIPLY = info["MULTIPLY"]
# MULTIPLY1 = info["MULTIPLY1"]
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


#depth = client.get_order_book(symbol='KNCUSDT') # tpuma stakan@
#pprint.pprint(depth) #tpuma stakan@

#trades = client.get_recent_trades(symbol='KNCUSDT') #verjin gorcrqner@
#pprint.pprint(trades)

#trades = client.get_historical_trades(symbol='KNCUSDT')
#trades = client.get_aggregate_trades(symbol='KNCUSDT' )
#pprint.pprint(trades)

print(" ask - bid ")
for coin in all_list_usdt:
    lst1 = []
    agg_trades = client.aggregate_trade_iter(symbol=f'{coin}USDT', start_str='15 minutes ago UTC')

    for i in agg_trades:
        lst1.append(i)
    # print(lst1)

    #hashvenq true ev false qanaknery
    Fls = 0
    Tru = 0
    qt_true, qt_false = 0, 0,

    for m in lst1:
        if m['m'] == True:
            Tru += 1
            qt_true += float(m['q'])

        elif m['m'] == False:
            Fls += 1
            qt_false += float(m["q"])


    if Fls > Tru*1.5:
        print("Coin-", coin)
        print("True=", Tru, "False=", Fls)
        print("qt_true=", qt_true, "qt_false=", qt_false)
        print("---------------")




# iterate over the trade iterator
# for trade in agg_trades:
#     print(trade)
    # do something with the trade data

# convert the iterator to a list
# note: generators can only be iterated over once so we need to call it again
# agg_trades = client.aggregate_trade_iter(symbol='PEOPLEUSDT', )
# agg_trade_list = list(agg_trades)

# example using last_id value
# agg_trades = client.aggregate_trade_iter(symbol='PEOPLEUSDT', last_id=23380478)
# agg_trade_list = list(agg_trades)
