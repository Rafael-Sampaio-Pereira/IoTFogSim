# import pandas as pd
# import matplotlib.pyplot as plt

# path = 'outputs/2023_09_27__23_45_04/datasets/smart_home_Energy Meter.csv'

# def plot_energy_meter_line_graph(file_path):
#     df = pd.read_csv(file_path)

#     df.plot(x='mesured energy (Kw)', y='Total tax revenue (% of GDP) (ICTD (2021))')

#     # plt.savefig('foo.png', bbox_inches='tight')


# # plot_energy_meter_line_graph(path)

# df = pd.read_csv(path, sep=';')
# # print(df.columns)
# price_date = df['time']
# price_close = df['mesured energy (Kw)']
# plt.plot(price_date.values, price_close.values, linestyle='solid')


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

plt.style.use('seaborn')

def animate():
    data = pd.read_csv('outputs/2023_09_27__01_07_30/datasets/smart_home_Energy Meter.csv', header=0, sep=';')
    data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')

    x = data['time']
    y1 = data['mesured energy (Kw)']


    plt.cla()
    plt.plot(x.values, y1.values, label='Energy Meter')


    plt.legend(loc='upper left')
    plt.tight_layout()

    # ani = FuncAnimation(plt.gcf(), animate, interval=61000)

    plt.tight_layout()
    # plt.show()
    plt.savefig('foo.png', bbox_inches='tight')

if __name__ == '__main__':
    animate()