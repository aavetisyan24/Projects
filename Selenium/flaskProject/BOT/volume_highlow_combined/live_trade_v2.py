import pprint
import requests
import websocket, datetime
import json
import api_key_secret as key
from binance.client import Client
# import multiprocessing
import winsound
# import time


while True:
    try:
        print("Connecting....")
        client = Client(key.API_KEY_FUT, key.API_SECRET_FUT)
        all_coins = key.COINS_LIST

        while True:
            print("=====================GLOBAL START=====================")
            UP = []
            DOWN = []
            up_count, down_count = 0, 0


            for c in key.COINS_LIST[0]:
                info = []
                # url1 = f"https://api.binance.com/api/v1/ticker/24hr?symbol={c}USDT"
                # response = requests.get(url1)
                candles = client.futures_klines(symbol=c + "USDT", interval=Client.KLINE_INTERVAL_4HOUR, limit=1)
                m = candles
                print(m, c)  # all information, uncomment for print
                # sym = c
                # percentage = (m['priceChangePercent'])
                # if float(percentage) >= 0:
                #     up_count += 1
                #     info.append(sym)
                #     info.append(float(percentage))
                #     UP.append(info)
                # else:
                #     down_count += 1
                #     info.append(sym)
                #     info.append(float(percentage))
                #     DOWN.append(info)

            def Sort(sub_li):
                return (sorted(sub_li, key=lambda x: x[1]))

            Sorted_UP = Sort(UP)
            Sorted_DOWN = Sort(DOWN)

            # print("UP is: ", Sort(UP))
            # print("DOWN is: ", Sort(DOWN))
            print("UP is: ", up_count, " -", Sorted_UP)
            print("DOWN is: ",down_count, " -", Sorted_DOWN)


            B = 0
            S = 0
            T = 0
            RB = 0
            RS = 0

            cikl = 15
            while cikl != 0:
                cikl -= 1
                print(f"Buy-{B} Sell-{S} Time-{T}")
                RB = B
                RS = S
                B = 0
                S = 0


                def inside_of_10(coin, list_of_sorted):  # function will check if coin is inside of 10
                    coin_inside = coin + "USDT"
                    for i in list_of_sorted[:10]:
                        if i[0] == coin_inside:
                            return True

                def avrg_price_last_125_min(coin, minute=125):
                    timings = Client.KLINE_INTERVAL_1MINUTE
                    candles = client.futures_klines(symbol=coin + "USDT", interval=timings, limit=minute + 1)  # will take last 126 1 min info
                    all_prices = 0
                    total_min = len(candles) - 1
                    for price in candles[:-1]:  # no need to take last price, which is current price in progress
                        all_prices += float(price[4])  # will take price
                    av_price = all_prices / total_min  # calculating avrg price of last provided 125 min candle stick
                    return av_price

                for coin in all_coins[0]:

                    #print("--------------------------------------------------------------------------------------------", coin)
                    # SOCKET1 = f"wss://stream.binance.com:9443/ws/{coin}usdt@aggTrade"
                    lst1 = list(client.aggregate_trade_iter(symbol=f"{coin.upper()}USDT", start_str='15 minutes ago UTC'))

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
                    TOKOS_BUYER = ((AVR_PRICE_BUYER * 2) / 100)
                    TOKOS_SELLER = ((AVR_PRICE_SELLER * 2) / 100)

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

                        if RINOK > 0:
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

                    average_price = avrg_price_last_125_min(coin)  # take current coin avrg price for 125 min

                    if up_count > 80 and RS > 80 and RINOK > 0 and (RINOK*PRICE) >= 50000 and AVR_VOL_F > AVR_VOL_T and \
                            TOTAL_QANAK_F > TOTAL_QANAK_T and float(m['p']) > (AVR_PRICE_BUYER + ((AVR_PRICE_BUYER * 0.1) / 100))\
                            and float(m['p']) > average_price and float(m['p']) < (average_price+(average_price*0.3/100)):
                        if inside_of_10(coin, Sorted_UP[-1:-len(Sorted_UP):-1]):
                            winsound.Beep(700, 700)
                            print(" RINOK > 0", RINOK, "PRC", PRICE)
                            print("AVR_PRICE_BUYER", AVR_PRICE_BUYER)
                            print("-----------------------", coin)
                            print("    ", "AVR_LOT_BUYER", "            AVR_LOT_SELLER")
                            print("    ", AVR_VOL_F, "   ", AVR_VOL_T)
                            print("    ", TOTAL_QANAK_F, "  gorcarq", "      ", TOTAL_QANAK_T, "  gorcarq")

                    elif down_count > 80 and RB > 80 and RINOK < 0 and (RINOK*PRICE) <= -50000 and AVR_VOL_F < AVR_VOL_T and \
                            TOTAL_QANAK_F < TOTAL_QANAK_T and float(m['p']) < (AVR_PRICE_SELLER - ((AVR_PRICE_SELLER * 0.1) / 100))\
                            and float(m['p']) < average_price and float(m['p']) > (average_price-(average_price*0.3/100)):
                        if inside_of_10(coin, Sorted_DOWN):
                            winsound.Beep(700, 700)
                            print(" RINOK < 0", RINOK, "PRC", PRICE)
                            print("AVR_PRICE_SELLER", AVR_PRICE_SELLER)
                            print("-----------------------", coin)
                            print("    ", "AVR_LOT_BUYER", "            AVR_LOT_SELLER")
                            print("    ", AVR_VOL_F, "   ", AVR_VOL_T)
                            print("    ", TOTAL_QANAK_F, "  gorcarq", "      ", TOTAL_QANAK_T, "  gorcarq")

                    if RINOK > 0:
                        B += 1
                        #print("-------------------------------------------------------------------------------F", coin)
                    else:
                        S += 1
                        #print("-------------------------------------------------------------------------------T", coin)
    except Exception as e:
        print("No connection")
        # time.sleep(5)
    pass
