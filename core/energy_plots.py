import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core.functions import get_last_dir_inside_of
from matplotlib import style
import pandas as pd
import os



def energy_live_plot():

    style.use('fivethirtyeight')

    file_path = get_last_dir_inside_of('outputs')+"/datasets/smart_home_Energy Meter.csv"
    if os.path.isfile(file_path):
        fig = plt.figure()
        fig.suptitle('Energy Monitor', fontsize=15)
        ax1 = fig.add_subplot(1,1,1)

        tail_length = 50

        def animate(i):
            graph_data = pd.read_csv(file_path, header=0, sep=';')
            graph_data[' time'] = pd.to_datetime(graph_data[' time'], format='%H:%M:%S')

            x = graph_data[' time'][-tail_length:]
            y1 = graph_data[' mesured energy (Kw)'][-tail_length:]

            ax1.clear()
            
            ax1.plot(
                x.values,
                y1.values,
                scaley=True,
                scalex=True,
                color="red",
                linewidth=1
            )
            ax1.set(xlabel="Time", ylabel="Energy consumption (KW)")
            ax1.xaxis.label.set_size(10)
            ax1.yaxis.label.set_size(10)
            ax1.tick_params(axis='both', which='major', labelsize=7)
        ani = animation.FuncAnimation(fig, animate, interval=1)

        plt.show()


def energy_stored_data_plot(amount=None):

    plt.style.use('seaborn')

    def animate():
        file_path = get_last_dir_inside_of('outputs')+"/datasets/smart_home_Energy Meter.csv"
        data = pd.read_csv(file_path, header=0, sep=';')
        data[' time'] = pd.to_datetime(data[' time'], format='%H:%M:%S')

        x = data[' time']
        y1 = data[' mesured energy (Kw)']

        plt.cla()
        plt.plot(x.values, y1.values, label=f'Energy Meter ({amount}Kw)' if amount else 'Energy Meter')
        plt.xlabel("Time")
        plt.ylabel("Energy Consumption (KW)")

        plt.legend(loc='upper left')
        plt.tight_layout()

        plt.tight_layout()

        # create graphics directoy if it not exist
        os.makedirs(get_last_dir_inside_of('outputs')+"/graphics/", exist_ok=True)

        plt.savefig(get_last_dir_inside_of('outputs')+'/graphics/total_energy_consumption.png', bbox_inches='tight')

    animate()