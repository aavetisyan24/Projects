# from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
#
# binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")
# binance_websocket_api_manager.create_stream('arr', '!userData', api_key="cEd9lEQacbpDlqMleeBYdEZFg7WhCW53chVxKXzG6kND1iGEKTiLF9AhZezvsjRg", api_secret="FFK4uFT8yaD3HGQVLjKHiUc0ffCIcSXL8P1rdK4jIyvRlbyjKwcXHjV2MYaFlgis", output="UnicornFy")
# while True:
#     data = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
#     if data:
#         print(data)
import websocket
import json, pprint
import sample_config
from binance.client import Client
import multiprocessing

client = Client(sample_config.API_KEY, sample_config.API_SECRET)


# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#general-wss-information
SOCKET1 = "wss://fstream.binance.com/stream?streams=ethusdt@bookTicker/ethbusd@bookTicker"
#wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@markPrice
# SOCKET2 = "wss://fstream.binance.com/stream?streams=ethusdt@bookTicker"
# SOCKET = "wss://fstream.binance.com/ws/bnbusdt@aggTrade"

def fut(SOCKET):

    def on_open(ws):
        print('opened connection')


    def on_close(ws):
        print("closed connection")


    def on_message(ws, message):
        # print("received message")
        # print(message)
        usdt, busd = "?", "?"
        json_message = json.loads(message)  # loading message to json file
        # pprint.pprint((json_message["data"]['s']))
        if json_message["data"]['s'] == "ETHUSDT":
            usdt = json_message["data"]['E']
        else:
            busd = json_message["data"]['E']

        print("USDT", usdt, "---------- " "BUSD", busd)




    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)  # create websoccet
    ws.run_forever()  # run websocket

p1 = multiprocessing.Process(target=fut(SOCKET1))
# p2 = multiprocessing.Process(target=fut(SOCKET2))

p1.start()
# p2.start()

p1.join()
# p2.join()

"""received message
{'E': 1619443860028,
 'e': 'kline',
 'k': {'B': '0',
       'L': 378382826,
       'Q': '1327735.19053720',
       'T': 1619443859999,
       'V': '532.18199000',
       'c': '2494.06000000',
       'f': 378382161,
       'h': '2496.00000000',
       'i': '1m',
       'l': '2492.84000000',
       'n': 666,
       'o': '2494.35000000',
       'q': '1885944.48228050',
       's': 'ETHUSDT',
       't': 1619443800000,  <-------------- unix time
       'v': '755.95549000',
       'x': True},       <------------- True means closed
 's': 'ETHUSDT'}"""


"""
  "e":"bookTicker",         // event type
  "u":400900217,            // order book updateId
  "E": 1568014460893,       // event time
  "T": 1568014460891,       // transaction time
  "s":"BNBUSDT",            // symbol
  "b":"25.35190000",        // best bid price  <---------------
  "B":"31.21000000",        // best bid qty  <------------
  "a":"25.36520000",        // best ask price <----------
  "A":"40.66000000"         // best ask qty <---------------
"""