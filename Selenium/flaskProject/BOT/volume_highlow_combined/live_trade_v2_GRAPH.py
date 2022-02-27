import websocket, datetime
import matplotlib.pyplot as plt
import api_key_secret as key
from binance.client import Client
import json
import csv
import time

filedname = ["TIME","PRICE", "AVPRICE", "RINOK"]
plt.style.use("fivethirtyeight")


client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)
all_coins = key.COINS_LIST
coin = 'people'


# print("-----------------------------------------------------------------------------------------------", coin)
SOCKET1 = f"wss://stream.binance.com:9443/ws/{coin}usdt@aggTrade"
agg_trades = client.aggregate_trade_iter(symbol=f"{coin.upper()}USDT", start_str='180minutes ago UTC')


lst1 = []
for i in agg_trades:
    # pprint.pprint(i)
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

TOTAL_OBYOM_F = 0.0001
TOTAL_QANAK_F = 1

QTY_SEL = 0.0
AVR_PRICE_SELLER = 0
total_caxs_seller = 0
SELLER_CAXSI_QANAK = 0
SELLER_QTY_QANAK = 0
SELLER_QTY_GUMAR = 0

TOTAL_OBYOM_T = 0.0001
TOTAL_QANAK_T = 1
AVR_VOL_F, AVR_VOL_T = 0, 0
PRICE = 0


jamanak = 0
with open("data.csv", "w") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=filedname)
    csv_writer.writeheader()

# while True:
with open("data.csv", "a") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=filedname)

    for m in lst1:
        PRICE = float(m['p'])  # price
        price = PRICE
        jamanak += 1

        if m['m'] == False:
            # print("-----------------------------------------------------", T)
            RINOK += float(m['q'])
            QTY_BUY = float(m['q'])
            PRICE_BUY = float(m['p'])
            caxs_buyer = float(m['q']) * float(m['p'])
            total_caxs_buyer += caxs_buyer
            # print("BUYER caxsac gumar",caxs_buyer,"---------","BUYER @ndhanur caxsac gumar",total_caxs_buyer)
            BUYER_CAXSI_QANAK += 1
            BUYER_QTY_QANAK += 1
            BUYER_QTY_GUMAR += QTY_BUY
            TOTAL_OBYOM_F += float(m['q'])
            TOTAL_QANAK_F += 1
        elif m['m'] == True:
            # print("-----------------------------------------------------", T)
            RINOK -= float(m['q'])
            QTY_SEL = float(m['q'])
            PRICE_SEL = float(m['p'])
            caxs_seller = float(m['q']) * float(m['p'])
            total_caxs_seller += caxs_seller
            # print("S caxsac gumar",caxs_seller,"---------","S @ndhanur caxsac gumar",total_caxs_seller)
            SELLER_CAXSI_QANAK += 1
            SELLER_QTY_QANAK += 1
            SELLER_QTY_GUMAR += QTY_SEL
            TOTAL_OBYOM_T += float(m['q'])
            TOTAL_QANAK_T += 1

        AVR_VOL_F = TOTAL_OBYOM_F / TOTAL_QANAK_F
        AVR_VOL_T = TOTAL_OBYOM_T / TOTAL_QANAK_T

        if RINOK > 0:
            total_caxs_seller = 0
            AVR_PRICE_SELLER = 0
            SELLER_QTY_GUMAR = 0
            SELLER_QTY_QANAK = 0
            SELLER_CAXSI_QANAK = 0
            AVR_PRICE_BUYER = total_caxs_buyer / BUYER_QTY_GUMAR
            avprice = AVR_PRICE_BUYER

        elif RINOK < 0:
            total_caxs_buyer = 0
            AVR_PRICE_BUYER = 0
            BUYER_QTY_GUMAR = 0
            BUYER_QTY_QANAK = 0
            BUYER_CAXSI_QANAK = 0
            AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR
            avprice = AVR_PRICE_SELLER


        rinok = RINOK

        info = {
            "TIME": jamanak,
            "PRICE": price,
            "AVPRICE": avprice,
            "RINOK": rinok
        }
        csv_writer.writerow(info)
        print(jamanak, price, avprice, rinok)
    time.sleep(1)


def on_open(ws):
    print('opened connection')

def on_close(ws):
    print("closed connection")

def on_message(ws, message):

    global RINOK, QTY_BUY, AVR_PRICE_BUYER, total_caxs_buyer, BUYER_CAXSI_QANAK, BUYER_QTY_QANAK, BUYER_QTY_GUMAR, \
        QTY_SEL, AVR_PRICE_SELLER, total_caxs_seller, SELLER_CAXSI_QANAK, SELLER_QTY_QANAK, SELLER_QTY_GUMAR, \
        TOTAL_OBYOM_T,  TOTAL_OBYOM_F, TOTAL_QANAK_F, TOTAL_QANAK_T, jamanak, PRICE, price, avprice, rinok, info

    m = json.loads(message)

    PRICE = float(m['p'])  # price
    price = PRICE
    jamanak += 1

    with open("data.csv", "a") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=filedname)

        if m['m'] == False:
            # print("-----------------------------------------------------", T)
            RINOK += float(m['q'])
            QTY_BUY = float(m['q'])
            caxs_buyer = float(m['q']) * float(m['p'])
            total_caxs_buyer += caxs_buyer
            # print("BUYER caxsac gumar",caxs_buyer,"---------","BUYER @ndhanur caxsac gumar",total_caxs_buyer)
            BUYER_CAXSI_QANAK += 1
            BUYER_QTY_QANAK += 1
            BUYER_QTY_GUMAR += QTY_BUY
            TOTAL_OBYOM_F += float(m['q'])
            TOTAL_QANAK_F += 1
        elif m['m'] == True:
            # print("-----------------------------------------------------", T)
            RINOK -= float(m['q'])
            QTY_SEL = float(m['q'])
            caxs_seller = float(m['q']) * float(m['p'])
            total_caxs_seller += caxs_seller
            # print("S caxsac gumar",caxs_seller,"---------","S @ndhanur caxsac gumar",total_caxs_seller)
            SELLER_CAXSI_QANAK += 1
            SELLER_QTY_QANAK += 1
            SELLER_QTY_GUMAR += QTY_SEL
            TOTAL_OBYOM_T += float(m['q'])
            TOTAL_QANAK_T += 1

        if RINOK > 0:
            total_caxs_seller = 0
            AVR_PRICE_SELLER = 0
            SELLER_QTY_GUMAR = 0
            SELLER_QTY_QANAK = 0
            SELLER_CAXSI_QANAK = 0
            AVR_PRICE_BUYER = total_caxs_buyer / BUYER_QTY_GUMAR
            avprice = AVR_PRICE_BUYER

        elif RINOK < 0:
            total_caxs_buyer = 0
            AVR_PRICE_BUYER = 0
            BUYER_QTY_GUMAR = 0
            BUYER_QTY_QANAK = 0
            BUYER_CAXSI_QANAK = 0
            AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR
            avprice = AVR_PRICE_SELLER

        rinok = RINOK

        info = {
            "TIME": jamanak,
            "PRICE": price,
            "AVPRICE": avprice,
            "RINOK": rinok
        }
        csv_writer.writerow(info)
        print(jamanak, price, avprice, rinok)


ws = websocket.WebSocketApp(SOCKET1, on_open=on_open, on_close=on_close, on_message=on_message)  # create websoccet
ws.run_forever()  # run websocket
