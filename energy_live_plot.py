import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import sys
import os

style.use('fivethirtyeight')


def main(file_path):
    if os.path.isfile(file_path):
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)

        tail_length = 50

        def animate(i):
            graph_data = pd.read_csv(file_path, header=0, sep=';')
            graph_data[' time'] = pd.to_datetime(graph_data[' time'], format='%H:%M:%S')

            x = graph_data[' time'][-tail_length:]
            y1 = graph_data[' mesured energy (Kw)'][-tail_length:]


            ax1.clear()
            ax1.plot(x.values, y1.values, scaley=True, scalex=True, color="red")

        ani = animation.FuncAnimation(fig, animate, interval=1)
        plt.show()

if __name__ == "__main__":
    main(sys.argv[1])