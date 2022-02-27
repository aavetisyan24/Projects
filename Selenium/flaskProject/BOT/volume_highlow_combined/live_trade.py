import websocket, datetime
import json, pprint
import api_key_secret as key
from binance.client import Client
import multiprocessing

client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)
coin = "people"



# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#general-wss-information
SOCKET1 = f"wss://stream.binance.com:9443/ws/{coin}usdt@aggTrade"
#wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@markPrice
# SOCKET2 = "wss://fstream.binance.com/stream?streams=ethusdt@bookTicker"
# SOCKET = "wss://fstream.binance.com/ws/bnbusdt@aggTrade"

# def fut(SOCKET):

candles = client.get_klines(symbol=f'{coin.upper()}USDT', interval=Client.KLINE_INTERVAL_1MINUTE)
# pprint.pprint(candles[-60:-5])

lst1 = []
agg_trades = client.aggregate_trade_iter(symbol=f"{coin.upper()}USDT", start_str='1 minutes ago UTC')

for i in agg_trades:
    lst1.append(i)


def unix_to_datetime(t):
    return datetime.datetime.fromtimestamp(int(t[:-3])).strftime('%H:%M:%S')

RINOK = 0.0

QTY_BUY = 0.0
AVR_PRICE_BUYER = 0
total_caxs_buyer = 0
BUYER_CAXSI_QANAK = 0
BUYER_QTY_QANAK = 0
BUYER_QTY_GUMAR = 0



QTY_SEL = 0.0
AVR_PRICE_SELLER = 0
total_caxs_seller = 0
SELLER_CAXSI_QANAK = 0
SELLER_QTY_QANAK = 0
SELLER_QTY_GUMAR = 0


for m in lst1:
    T = unix_to_datetime(str(m['T']))
    if m['m'] == False:
        print("-----------------------------------------------------", T, file=open("output.txt", "a"))
        RINOK += float(m['q'])
        QTY_BUY = float(m['q'])
        PRICE_BUY = float(m['p'])
        caxs_buyer = float(m['q'])*float(m['p'])
        total_caxs_buyer += caxs_buyer
        print("BUYER caxsac gumar",caxs_buyer,"---------","BUYER @ndhanur caxsac gumar",total_caxs_buyer)
        BUYER_CAXSI_QANAK += 1
        BUYER_QTY_QANAK += 1
        BUYER_QTY_GUMAR += QTY_BUY
    elif m['m'] == True:
        print("-----------------------------------------------------", T)
        RINOK -= float(m['q'])
        QTY_SEL = float(m['q'])
        PRICE_SEL = float(m['p'])
        caxs_seller = float(m['q'])*float(m['p'])
        total_caxs_seller += caxs_seller
        print("S caxsac gumar",caxs_seller,"---------","S @ndhanur caxsac gumar",total_caxs_seller)
        SELLER_CAXSI_QANAK += 1
        SELLER_QTY_QANAK += 1
        SELLER_QTY_GUMAR += QTY_SEL


    if RINOK > 0 and m['m'] == False:
        total_caxs_seller = 0
        AVR_PRICE_SELLER = 0
        SELLER_QTY_GUMAR = 0
        SELLER_QTY_QANAK = 0
        SELLER_CAXSI_QANAK = 0
        AVR_PRICE_BUYER = total_caxs_buyer/BUYER_QTY_GUMAR

        print(" RINOK > 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
        print("-----------------------")
    elif RINOK > 0 and m['m'] == True:
        total_caxs_seller = 0
        AVR_PRICE_SELLER = 0
        SELLER_QTY_GUMAR = 0
        SELLER_QTY_QANAK = 0
        SELLER_CAXSI_QANAK = 0
        AVR_PRICE_BUYER = total_caxs_buyer / BUYER_QTY_GUMAR

        print(" RINOK > 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
        print("-----------------------")
    elif RINOK < 0 and m['m'] == True:
        total_caxs_buyer = 0
        AVR_PRICE_BUYER = 0
        BUYER_QTY_GUMAR = 0
        BUYER_QTY_QANAK = 0
        BUYER_CAXSI_QANAK = 0
        AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR

        print(" RINOK < 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
        print("-----------------------")
    elif RINOK < 0 and m['m'] == False:
        total_caxs_buyer = 0
        AVR_PRICE_BUYER = 0
        BUYER_QTY_GUMAR = 0
        BUYER_QTY_QANAK = 0
        BUYER_CAXSI_QANAK = 0
        AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR

        print(" RINOK < 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
        print("-----------------------")


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global RINOK, QTY_BUY, AVR_PRICE_BUYER, total_caxs_buyer, BUYER_CAXSI_QANAK, BUYER_QTY_QANAK, BUYER_QTY_GUMAR, \
        QTY_SEL, AVR_PRICE_SELLER, total_caxs_seller, SELLER_CAXSI_QANAK, SELLER_QTY_QANAK, SELLER_QTY_GUMAR


    m = json.loads(message)
    TIME = unix_to_datetime(str(m['T']))

    if m['m'] == False:

        RINOK += float(m['q'])
        QTY_BUY = float(m['q'])
        # PRICE_BUY = float(m['p'])
        caxs_buyer = float(m['q']) * float(m['p'])
        total_caxs_buyer += caxs_buyer
        print("BUYER caxsac gumar", caxs_buyer, "---------", "BUYER @ndhanur caxsac gumar", total_caxs_buyer)
        BUYER_CAXSI_QANAK += 1
        BUYER_QTY_QANAK += 1
        BUYER_QTY_GUMAR += QTY_BUY
    elif m['m'] == True:
        RINOK -= float(m['q'])
        QTY_SEL = float(m['q'])
        # PRICE_SEL = float(m['p'])
        caxs_seller = float(m['q']) * float(m['p'])
        total_caxs_seller += caxs_seller
        print("S caxsac gumar", caxs_seller, "---------", "S @ndhanur caxsac gumar", total_caxs_seller)
        SELLER_CAXSI_QANAK += 1
        SELLER_QTY_QANAK += 1
        SELLER_QTY_GUMAR += QTY_SEL

    if RINOK > 0 and m['m'] == False:
        total_caxs_seller = 0
        AVR_PRICE_SELLER = 0
        SELLER_QTY_GUMAR = 0
        SELLER_QTY_QANAK = 0
        SELLER_CAXSI_QANAK = 0
        AVR_PRICE_BUYER = total_caxs_buyer / BUYER_QTY_GUMAR
        print(" RINOK > 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
        print("-----------------------")
    elif RINOK > 0 and m['m'] == True:
        total_caxs_seller = 0
        AVR_PRICE_SELLER = 0
        SELLER_QTY_GUMAR = 0
        SELLER_QTY_QANAK = 0
        SELLER_CAXSI_QANAK = 0
        AVR_PRICE_BUYER = total_caxs_buyer / BUYER_QTY_GUMAR
        print(" RINOK > 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
        print("-----------------------")
    elif RINOK < 0 and m['m'] == True:
        total_caxs_buyer = 0
        AVR_PRICE_BUYER = 0
        BUYER_QTY_GUMAR = 0
        BUYER_QTY_QANAK = 0
        BUYER_CAXSI_QANAK = 0
        AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR
        print(" RINOK < 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
        print("-----------------------")
    elif RINOK < 0 and m['m'] == False:
        total_caxs_buyer = 0
        AVR_PRICE_BUYER = 0
        BUYER_QTY_GUMAR = 0
        BUYER_QTY_QANAK = 0
        BUYER_CAXSI_QANAK = 0
        AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR
        print(" RINOK < 0", RINOK, "PRC", m['p'], "QTY", m['q'], '      ', m['m'])
        print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
        print("-----------------------")

    print("-----------------------------------------------------", TIME)


ws = websocket.WebSocketApp(SOCKET1, on_open=on_open, on_close=on_close, on_message=on_message)  # create websoccet
ws.run_forever()  # run websocket
