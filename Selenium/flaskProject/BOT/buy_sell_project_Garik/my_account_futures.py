import pprint
import time
from datetime import datetime
import pandas as pd
import api_key_secret as key
from binance.client import Client
import json
import logging

from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
logging.basicConfig(filename="history.log", level=logging.INFO)

api_key = key.API_KEY_FUT
api_secret = key.API_SECRET_FUT

client = Client(api_key, api_secret)

## main

# get balances for all assets & some account information
# pprint.pprint(client.get_account())
#
# # get balance for a specific asset only (BTC)
# print(client.get_asset_balance(asset='USD'))

# get balances for futures account
# pprint.pprint(client.futures_get_all_orders())

# get balances for margin account
# will raise an exception if margin account is not activated
#print(client.get_margin_account())

def sell_order_market(symbol="DOGEUSDT", quantity=40):
    order_info = []
    run_time = datetime.now()
    sell_order = client.futures_create_order(
        symbol=symbol,
        type=ORDER_TYPE_LIMIT,
        side=SIDE_SELL,
        quantity=quantity
    )
    end_time = datetime.now()
    order_info.append(run_time)
    order_info.append(end_time)
    order_info.append(sell_order)
    logging.info(order_info)
    print("Success!")


def order_limit(symbol="DOGEUSDT", quantity=40):
    order_info = []
    run_time = datetime.now()
    sell_order = client.create_test_order(
        symbol=symbol,
        type=FUTURE_ORDER_TYPE_LIMIT,
        timeInForce="GTC",
        side=SIDE_SELL,
        quantity=quantity,
        price=0.1610
    )
    end_time = datetime.now()
    order_info.append(run_time)
    order_info.append(end_time)
    order_info.append(sell_order)
    logging.info(order_info)
    print("Success!")

# order_limit()
# buy_order_limit = client.create_test_order(
#     symbol='DOGEUSDT',
#     side='BUY',
#     type=ORDER_TYPE_MARKET,
#     # timeInForce='GTC',
#     quantity=100)
#     # price=200)
# print(buy_order_limit)

# into a pandas DataFrame for neater output
# df = pd.DataFrame(
#     client.futures_order_book(symbol='DOGEUSDT')
# )
# print(df[['bids', 'asks']].head())
# client.futures_change_leverage(symbol='DOGEUSDT', leverage=1)

def order_market(SIDE=SIDE_BUY, symbol="DOGEUSDT", quantity=40):
    order_info = []
    run_time = datetime.now()
    sell_order = client.futures_create_order(
        symbol=symbol,
        type=ORDER_TYPE_LIMIT,
        side=SIDE,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=0.161
    )
    end_time = datetime.now()
    order_info.append(run_time)
    order_info.append(end_time)
    order_info.append(sell_order)
    logging.info(order_info)
    print("Success!")

order_market()