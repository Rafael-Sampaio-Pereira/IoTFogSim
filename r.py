# import random
# import time

# import matplotlib.pyplot as plt


# def simulate_5g_latency_for_smart_grids():
#     # the paper "A Survey on Low Latency Towards 5G: RAN, Core Network and Caching Solutions"(Parvaez, 2017) shows that
#     # latency requirements for smart grids under 5g networks is between 1 and 20ms - Rafael Sampaio

#     suitable_latency_values = []

#     # x = random.gammavariate(0.001, 0.02)
#     x = random.gammavariate(0.1, 3)
#     x = round(x, 3)
#     print(x)
#     suitable_latency_values.append(x)
#     return x

#     # latency = random.choice(suitable_latency_values)
#     # time.sleep(latency)


# suitable_latency_values = []
# for i in range(1000):
#     value = simulate_5g_latency_for_smart_grids()
#     suitable_latency_values.append(value)


# # create plot of Gamma distribution
# plt.plot(suitable_latency_values)

# # display plot
# plt.show()


import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

x = np.linspace(0, 10)
y = stats.gamma.pdf(x, a=5, scale=0.333)
print(y)
plt.plot(x, y, "ro-", label=(r'$\alpha=0, \beta=3$'))
plt.legend(loc='upper right')

plt.show()
