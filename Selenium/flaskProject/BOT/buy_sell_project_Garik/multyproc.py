import websocket
import json, pprint
import sample_config
from binance.client import Client
import datetime, winsound

client = Client(sample_config.API_KEY, sample_config.API_SECRET)

SOCKET1 = "wss://fstream.binance.com/stream?streams=dogebusd@bookTicker/dogeusdt@bookTicker"

usdt = False
busd = False
list_info_usdt, list_info_busd = False, False
value = 0.015  # 0.015%


def fut(SOCKET):

    def sound():
        winsound.Beep(500, 50)

    def unix_to_datetime(t):
        return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M:%S')

    def on_open(ws):
        print('opened connection')

    def on_close(ws):
        print("closed connection")

    def on_message(ws, message):
        global usdt, busd, list_info_usdt, list_info_busd, value
        # print("received message")
        # print(message)
        json_message = json.loads(message)  # loading message to json file
        # print(json_message['E'])
        runtime = unix_to_datetime(str(json_message["data"]['E']))
        # usdt, busd = False, False

        if json_message["data"]['s'] == "DOGEUSDT": # and (usdt == False):
            list_info_usdt = ((json_message["data"]['s'], (runtime), json_message["data"]['a'],json_message["data"]['A'],
                       "-----",json_message["data"]['b'],json_message["data"]['B']))
            print(1, list_info_usdt)
            usdt = True

        if json_message["data"]['s'] == "DOGEBUSD": # and busd == False:
            list_info_busd = ((json_message["data"]['s'], (runtime), json_message["data"]['a'],json_message["data"]['A'],
                       "-----",json_message["data"]['b'],json_message["data"]['B']))
            # print(2, list_info_busd)
            busd = True

        if usdt and busd:
            usdt = False
            busd = False
            # print("Pair created")
            usdt_ask, usdt_bid = float(list_info_usdt[2]), float(list_info_usdt[5])
            busd_ask, busd_bid = float(list_info_busd[2]), float(list_info_busd[5])

            # print("USDT-ask-",usdt_ask, "-bid-",usdt_bid)
            # print("BUSD-bid-",busd_bid, "-ask-",busd_ask)
            # print(type(usdt_ask), type(usdt_bid), type(busd_ask), type(busd_bid))

            if usdt_ask < busd_bid-(busd_bid*0.0003) or busd_ask < usdt_bid-(usdt_bid*0.0003):
                print("Pair created")
                print("USDT-ask-", usdt_ask, "-bid-", usdt_bid)
                print("BUSD-bid-", busd_bid, "-ask-", busd_ask)
                print("----------------------------------------------------")
                sound()


            # print("===============================")



    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)  # create websoccet
    ws.run_forever()  # run websocket



if __name__=="__main__":
    fut(SOCKET1)