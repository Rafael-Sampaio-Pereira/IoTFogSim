
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from datetime import datetime

# plt.style.use('seaborn')

# def animate():
#     data = pd.read_csv('outputs/2023_10_03__13_54_22/datasets/smart_home_Energy Meter.csv', header=0, sep=';')
#     data[' time'] = pd.to_datetime(data[' time'], format='%H:%M:%S')

#     x = data[' time']
#     y1 = data[' mesured energy (Kw)']


#     plt.cla()
#     plt.plot(x.values, y1.values, label='Energy Meter')


#     plt.legend(loc='upper left')
#     plt.tight_layout()

#     # ani = FuncAnimation(plt.gcf(), animate, interval=1000)

#     plt.tight_layout()
#     # plt.show()
#     plt.savefig('foo.png', bbox_inches='tight')

# if __name__ == '__main__':
#     animate()

# =================================================================

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import pathlib, os

style.use('fivethirtyeight')

fig = plt.figure()
# fig.gca().relim()
# fig.gca().autoscale_view()
ax1 = fig.add_subplot(1,1,1)

tail_length = 50


def get_last_dir_inside_of(directory):
    return str(max(pathlib.Path(directory).glob('*/'), key=os.path.getmtime))


def animate(i):
    file = get_last_dir_inside_of('outputs')+"/datasets/smart_home_Energy Meter.csv"
    graph_data = pd.read_csv(file, header=0, sep=';')
    graph_data[' time'] = pd.to_datetime(graph_data[' time'], format='%H:%M:%S')

    x = graph_data[' time'][-tail_length:]
    y1 = graph_data[' mesured energy (Kw)'][-tail_length:]


    ax1.clear()
    ax1.plot(x.values, y1.values, scaley=True, scalex=True, color="red")

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

# =================================================================


# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import random
# import pandas as pd
# # %matplotlib qt

# fig = plt.figure(figsize=(6,4))
# axes = fig.add_subplot(1,1,1)
# plt.title("Dynamic Axes")

# tail_length = 50


# def animate(i):
#     graph_data = pd.read_csv('outputs/2023_10_03__23_23_21/datasets/smart_home_Energy Meter.csv', header=0, sep=';')
#     graph_data[' time'] = pd.to_datetime(graph_data[' time'], format='%H:%M:%S')

#     x = graph_data[' time'][-tail_length:]
#     y1 = graph_data[' mesured energy (Kw)'][-tail_length:]
#     plt.xlim(i-30,i+3)
#     axes.set_ylim(y1[i]-100, y1[i]+100)
#     plt.plot(x,y1, scaley=True, scalex=True, color="red")

# anim = FuncAnimation(fig, animate, interval=100)

# plt.show()


