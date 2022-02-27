import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd


def animate(i):
    data = pd.read_csv("data.csv")

    D_JAMANAK = data['TIME']
    D_PRICE = data['PRICE']
    D_AVPRICE = data['AVPRICE']
    D_RINOK = data["RINOK"]

    plt.cla()

    #plot1
    plt.subplot(2, 1, 1)
    plt.plot(D_JAMANAK, D_PRICE, color='red', label='price')
    plt.plot(D_JAMANAK, D_AVPRICE, color='blue', label='avprice')


    #plot2
    plt.subplot(2, 1, 2)
    plt.plot(D_JAMANAK, D_RINOK, color='green', label='rinok')
    plt.plot(D_JAMANAK, D_RINOK*0, color='black')


    # plt.legend(loc='upper right')
    plt.tight_layout()
    # plt.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
