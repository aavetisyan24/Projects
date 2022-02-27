import pprint
import requests
import websocket, datetime
import json
import api_key_secret as key
from binance.client import Client
# import multiprocessing
import winsound


client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)
all_coins = key.COINS_LIST


coin1 = "XRP"
coin2 = "DOGE"
#test 1

print(datetime.datetime.now())
lst1 = list(client.aggregate_trade_iter(symbol=f"{coin1.upper()}USDT", start_str='15 minutes ago UTC'))
# print("list1",lst1)
print(datetime.datetime.now())

#test 2
print(datetime.datetime.now())
# lst2 = []
agg_trade = list(client.aggregate_trade_iter(symbol=f"{coin2.upper()}USDT", start_str='15 minutes ago UTC'))
lst2 = [e for e in agg_trade]
# print("list2",lst2)
print(datetime.datetime.now())
