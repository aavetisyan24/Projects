import time

import api_key_secret as key
from binance.client import Client
from binance.enums import *
client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)


def buy(symbol, quantity):
    try:
        print("+++++++++ORDER BUY++++++++++")
        print("+   sending     order      +")
        order = client.futures_create_order(symbol=symbol,
                                               side=SIDE_BUY,
                                               type=ORDER_TYPE_MARKET,
                                               quantity=quantity)
        print("+  Limit Order have been sent!    +")
        print("+     Limit order details         +", order)
        order_id = order["orderId"]
        print("+      Limit order ID is----------+", order_id)
        print("+++++++++++++++++++++++++++++++++++")
    except Exception as e:
        print(e)


def stop_lose(symbol, stopPrice):
    FuturesStopLoss =client.futures_create_order(
      symbol=symbol,
      type=FUTURE_ORDER_TYPE_STOP_MARKET,
      side=SIDE_SELL,
      stopPrice=stopPrice,
      closePosition=True
      )
    print(FuturesStopLoss)


def take_profit(symbol, takeProfitprice):
    FuturesTakeprofit = client.futures_create_order(
      symbol=symbol,
      type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET,
      side=SIDE_SELL,
      stopPrice=takeProfitprice,
      closePosition=True
      )
    print(FuturesTakeprofit)


def buy_market(coin, rnd):
    all_info = client.futures_position_information()
    for info in all_info:
        if float(info["positionAmt"]) != 0 and info["symbol"] == coin+"USDT":
            entryPrice = float(info["entryPrice"])
            stoplose = round(entryPrice-(entryPrice*0.5/100), rnd)
            takePrice = round(entryPrice+(entryPrice*1.5/100), rnd)
            sym = info['symbol']
            print(f'entryprice = {entryPrice}, stoploss = {stoplose}, takePrice = {takePrice}, symbole = {sym}')
            stop_lose(sym, stoplose)
            time.sleep(3)
            take_profit(sym, takeProfitprice=takePrice)


def calc_round(price):  # calculating round
    rnd = len(str(price).split(".")[-1])
    return rnd


def my_qty(price):
    rnd = 0
    x = str(6/price).split(".")
    print(x)
    if x[0] == "0":
        for i in x[1]:
            if i == "0":
                rnd += 1
            else:
                return rnd+1
    return 1



# order = client.futures_create_order(
#             symbol='ETHUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=quantity, isolated=True, positionSide=positionSide)
#         client.futures_create_order(
#             symbol='ETHUSDT', side=SIDE_SELL, type=FUTURE_ORDER_TYPE_STOP_MARKET, quantity=quantity, positionSide=positionSide, stopPrice=stopLoss, timeInForce=TIME_IN_FORCE_GTC)
#         client.futures_create_order(
#             symbol='ETHUSDT', side=SIDE_SELL, type=FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET, quantity=quantity, positionSide=positionSide, stopPrice=takeProfit, timeInForce=TIME_IN_FORCE_GTC)
#


# {'entryPrice': '0.14472',
#   'isAutoAddMargin': 'false',
#   'isolatedMargin': '0.00000000',
#   'isolatedWallet': '0',
#   'leverage': '1',
#   'liquidationPrice': '0',
#   'marginType': 'cross',
#   'markPrice': '0.14514000',
#   'maxNotionalValue': '5.0E7',
#   'notional': '5.80560000',
#   'positionAmt': '40',
#   'positionSide': 'BOTH',
#   'symbol': 'DOGEUSDT',
#   'unRealizedProfit': '0.01680000',
#   'updateTime': 1644684556918},

#
# try:
#     print("+++++++++ORDER LIMIT SELL++++++++++")
#     print("+   sending limit_sell order      +")
#     order_limit = self.client.create_order(symbol=symbol,
#                                            side=SIDE_SELL,
#                                            type=ORDER_TYPE_STOP_LOSS_LIMIT,
#                                            timeInForce=TIME_IN_FORCE_GTC,
#                                            quantity=quantity,
#                                            price=price,
#                                            stopPrice=stopPrice)
#     print("+  Limit Order have been sent!    +")
#     print("+     Limit order details         +", order_limit)
#     limit_sell_order_id = order_limit["orderId"]
#     print("+      Limit order ID is----------+", limit_sell_order_id)
#     print("+++++++++++++++++++++++++++++++++++")
#     self.limit_sell_order_id = limit_sell_order_id