import websocket
import json, pprint
import sample_config
from binance.client import Client
import datetime

client = Client(sample_config.API_KEY, sample_config.API_SECRET)

SOCKET2 = "wss://fstream.binance.com/ws/ethbusd@bookTicker"

def fut(SOCKET):

    def unix_to_datetime(t):
        return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M:%S')

    def on_open(ws):
        print('opened connection')

    def on_close(ws):
        print("closed connection")

    def on_message(ws, message):
        # print("received message")
        # print(message)
        json_message = json.loads(message)  # loading message to json file
        # print(json_message['E'])
        runtime = unix_to_datetime(str(json_message['E']))
        pprint.pprint((json_message['s'], (runtime)))

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)  # create websoccet
    ws.run_forever()  # run websocket



if __name__=="__main__":
    fut(SOCKET2)