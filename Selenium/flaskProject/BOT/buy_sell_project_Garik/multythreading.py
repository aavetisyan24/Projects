import time
import websocket, datetime, json
from binance.client import Client
from binance.enums import *
from threading import *
import api_key_secret as key
import logging
# from datetime import datetime
logging.basicConfig(filename="history.log", level=logging.INFO)
api_key = key.API_KEY_FUT
api_secret = key.API_SECRET_FUT
client = Client(api_key, api_secret)


list_info_usdt = []
list_info_busd = []

class Futures1(Thread):

    def __init__(self, socket_name):
        super().__init__()
        self.socket_name = socket_name
        self.coin = coin

    def unix_to_datetime(self, t):
        return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M:%S')

    def on_open(self, ws):
        print('opened connection')

    def on_close(self, ws):
        print("closed connection")

    def on_message(self, ws, message):
        global list_info_usdt
        msg = json.loads(message)  # loading message to json file
        data = msg["data"]
        runtime = self.unix_to_datetime(str(data['E']))
        list_info_usdt = [data['s'], runtime, data['a'], data['A'], "|||||||", data['b'], data['B']]

        # print(runtime)

    def run(self):
        ws = websocket.WebSocketApp(self.socket_name, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)  # create websoccet
        ws.run_forever()  # run websocket


class Futures2(Thread):

    def __init__(self, socket_name):
        super().__init__()
        self.socket_name = socket_name
        self.coin = coin

    def unix_to_datetime(self, t):
        return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M:%S')

    def on_open(self, ws):
        print('opened connection')

    def on_close(self, ws):
        print("closed connection")

    def on_message(self, ws, message):
        global list_info_busd
        # print("received message")
        msg = json.loads(message)  # loading message to json file
        data = msg["data"]
        runtime = self.unix_to_datetime(str(data['E']))
        list_info_busd = [data['s'], runtime, data['a'], data['A'], "|||||||", data['b'], data['B']]

    def run(self):
        ws = websocket.WebSocketApp(self.socket_name, on_open=self.on_open, on_close=self.on_close,
                                    on_message=self.on_message)  # create websoccet
        ws.run_forever()  # run websocket

def order_market(SIDE, symbol, quantity=40):
    order_info = []
    # run_time = datetime.now()
    sell_order = client.futures_create_order(
        symbol=symbol,
        type=ORDER_TYPE_MARKET,
        side=SIDE,
        quantity=quantity
    )
    # end_time = datetime.now()
    # order_info.append(run_time)
    # order_info.append(end_time)
    order_info.append(sell_order)
    logging.info(order_info)
    print("Success!")


if __name__=="__main__":
    DO_IT = True
    CHECKFORCLOSE = False
    CLOSE = True
    coin = "doge"
    Bot1 = Futures1(f"wss://fstream.binance.com/stream?streams={coin}usdt@bookTicker")
    Bot2 = Futures2(f"wss://fstream.binance.com/stream?streams={coin}busd@bookTicker")
    (Bot1.start())
    (Bot2.start())
    while DO_IT:
        if list_info_usdt and list_info_busd:
            print("1",(list_info_usdt))
            print("2",(list_info_busd))
            usdt_ask, usdt_bid = float(list_info_usdt[2]), float(list_info_usdt[5])
            busd_ask, busd_bid = float(list_info_busd[2]), float(list_info_busd[5])
            if usdt_ask < busd_bid-(busd_bid*0.0004):# or busd_ask < usdt_bid-(usdt_bid*0.0003):
                print("Pair created")
                print("USDT-ask-", usdt_ask, "-bid-", usdt_bid)
                print("BUSD-bid-", busd_bid, "-ask-", busd_ask)
                order_market(SIDE_SELL, "DOGEBUSD", quantity=40)
                order_market(SIDE_BUY, "DOGEUSDT", quantity=40)

                # logging.info("USDT-ask-", str(usdt_ask), "-bid-", str(usdt_bid))
                # logging.info("BUSD-bid-", str(busd_bid), "-ask-", str(busd_ask))
                print("--------------------------------------------Order Buy and Sell have been sent!!!")
                DO_IT = False

            # list_info_usdt, list_info_busd = [], []

    print("checking to close....")
    time.sleep(3)  #sleeping to make sure lists are updated
    while not DO_IT and CLOSE:
        # print("1", (list_info_usdt))
        # print("2", (list_info_busd))
        usdt_bid = float(list_info_usdt[5])
        busd_ask = float(list_info_busd[2])
        if usdt_bid >= busd_ask+(busd_ask*0.0001):
            order_market(SIDE_BUY, "DOGEBUSD", quantity=40)
            order_market(SIDE_SELL, "DOGEUSDT", quantity=40)
            print("USDT bid", usdt_bid)
            print("BUSD ask", busd_ask)
            print(".......................Closed!")
            CLOSE = False
            break




