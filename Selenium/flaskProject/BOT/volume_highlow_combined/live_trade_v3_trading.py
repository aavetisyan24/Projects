import time
import websocket, datetime
# import json
# import api_key_secret as key
# from binance.client import Client
# import multiprocessing
import winsound
from trade_functions import *

client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)
all_coins = key.COINS_LIST

MY_QTY = 0
B = 0
S = 35
T = 0
trade = True
gorcarq_buy = False
gorcarq_sell = False
rezerv_B, rezerv_S = 0, 0

while True:
    print("#########",B, S, T)
    rezerv_B = B
    rezerv_S = S
    print(f'box B = {rezerv_B},  box S = {rezerv_S}')
    B = 0
    S = 0


    for coin in all_coins[0]:

        #print("-----------------------------------------------------------------------------------------------", coin)
        SOCKET1 = f"wss://stream.binance.com:9443/ws/{coin}usdt@aggTrade"
        agg_trades = client.aggregate_trade_iter(symbol=f"{coin.upper()}USDT", start_str='135 minutes ago UTC')

        lst1 = []
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
        TOKOS_BUYER = ((AVR_PRICE_BUYER * 1) / 100)
        TOKOS_SELLER = ((AVR_PRICE_SELLER * 1) / 100)

        for m in lst1:
            PRICE = float(m['p'])
            T = unix_to_datetime(str(m['T']))
            if m['m'] == False:

                RINOK += float(m['q'])
                QTY_BUY = float(m['q'])
                PRICE_BUY = float(m['p'])
                caxs_buyer = float(m['q'])*float(m['p'])
                total_caxs_buyer += caxs_buyer

                BUYER_CAXSI_QANAK += 1
                BUYER_QTY_QANAK += 1
                BUYER_QTY_GUMAR += QTY_BUY
                TOTAL_OBYOM_F += float(m['q'])
                TOTAL_QANAK_F += 1
            elif m['m'] == True:

                RINOK -= float(m['q'])
                QTY_SEL = float(m['q'])
                PRICE_SEL = float(m['p'])
                caxs_seller = float(m['q'])*float(m['p'])
                total_caxs_seller += caxs_seller

                SELLER_CAXSI_QANAK += 1
                SELLER_QTY_QANAK += 1
                SELLER_QTY_GUMAR += QTY_SEL
                TOTAL_OBYOM_T += float(m['q'])
                TOTAL_QANAK_T += 1

            AVR_VOL_F = TOTAL_OBYOM_F / TOTAL_QANAK_F
            AVR_VOL_T = TOTAL_OBYOM_T / TOTAL_QANAK_T

            if RINOK > 0 :
                total_caxs_seller = 0
                AVR_PRICE_SELLER = 0
                SELLER_QTY_GUMAR = 0
                SELLER_QTY_QANAK = 0
                SELLER_CAXSI_QANAK = 0
                AVR_PRICE_BUYER = total_caxs_buyer/BUYER_QTY_GUMAR

            elif RINOK < 0 :
                total_caxs_buyer = 0
                AVR_PRICE_BUYER = 0
                BUYER_QTY_GUMAR = 0
                BUYER_QTY_QANAK = 0
                BUYER_CAXSI_QANAK = 0
                AVR_PRICE_SELLER = total_caxs_seller / SELLER_QTY_GUMAR

        if RINOK > 0 and AVR_VOL_F > AVR_VOL_T and TOTAL_QANAK_F > TOTAL_QANAK_T and (RINOK*PRICE) >= 300000 and float(m['p']) > (AVR_PRICE_BUYER + ((AVR_PRICE_BUYER * 0.5) / 100)):
            winsound.Beep(700, 700)
            gorcarq_sell = True
            print(" RINOK > 0", RINOK, "PRC", PRICE)
            print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
            print("-----------------------", coin)
            print("    ", "AVR_LOT_BUYER", "            AVR_LOT_SELLER")
            print("    ", AVR_VOL_F, "   ", AVR_VOL_T)
            print("    ", TOTAL_QANAK_F, "  gorcarq", "      ", TOTAL_QANAK_T, "  gorcarq")
            if rezerv_B >= 80 and trade:
                print("selling...")
                # sell()

            gorcarq_sell = False
            # trade = False

        elif RINOK < 0: # and AVR_VOL_F < AVR_VOL_T and TOTAL_QANAK_F < TOTAL_QANAK_T and (RINOK*PRICE) <= -300000 and float(m['p']) < (AVR_PRICE_SELLER - ((AVR_PRICE_SELLER * 0.5) / 100)):
            winsound.Beep(700, 700)
            gorcarq_buy = True
            print(" RINOK < 0", RINOK, "PRC", PRICE)
            print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
            print("-----------------------", coin)
            print("    ", "AVR_LOT_BUYER", "            AVR_LOT_SELLER")
            print("    ", AVR_VOL_F, "   ", AVR_VOL_T)
            print("    ", TOTAL_QANAK_F, "  gorcarq", "      ", TOTAL_QANAK_T, "  gorcarq")
            print("rezerv S is :", rezerv_S, "trade is :", trade)
            if rezerv_S >= 35 and trade:
                rnd = calc_round(PRICE)
                print("buying...")
                MY_QTY = round(float(6/PRICE), my_qty(PRICE))
                print("calculated MY_QTY is :", MY_QTY)
                buy(symbol=coin+"USDT", quantity=MY_QTY)
                time.sleep(5)
                buy_market(coin, rnd)

                gorcarq_buy = False
                trade = False

        if RINOK > 0:
            B += 1
            #print("------------------------------------------------------------------------------------------------F", coin)
        else:
            S += 1
            #print("-------------------------------------------------------------------------------T", coin)



