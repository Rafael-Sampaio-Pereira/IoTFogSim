

from timeit import default_timer as timer
from datetime import timedelta
import time

import random
import matplotlib.pyplot as plt
import random
from random import choices



def simulate_celular_latency(mean, sigma):
    suitable_latency_values = []
    for i in range(100):
        x = random.gammavariate(mean, sigma)
        x = round(x,2)

        

        suitable_latency_values.append(x)

    # population = [0.0, random.choice(suitable_latency_values)]
    # # the 0.0 value has less probalblity than the random choiced value - Rafael Sampaio
    # weights = [1, 99]
    # y = choices(population, weights, k=10)
    
    return random.choice(suitable_latency_values)




aleat = []


fig = plt.figure()

for i in range(1000):
    # x = random.gammavariate(0.069, 2)
    # x = random.gammavariate(1, 60.56)
    # x = random.gammavariate(0.0512, 1.01)

    x = random.gammavariate(0.001, 0.02)
    # x = random.lognormvariate(20,2)
    print(round(x,2))
    aleat.append(x/1000)

    # x = simulate_celular_latency(1, 0.5)
    # x = simulate_celular_latency(0.069, 0.5)
    # aleat.append(x)

ax1 = fig.add_subplot(211)
ax1.set_xlabel('Requests')
ax1.set_ylabel('time(s)')
ax1.set_title('Gamma Distribution for Latency Simulation')
ax1.plot(aleat, '-b')


ax2 = fig.add_subplot(212)
ax2.set_ylabel('Requests')
ax2.set_xlabel('time(s)')
ax2.hist(aleat, bins=10)






print("===================================")

x = simulate_celular_latency(0.069, 1.01)
print(round(x,2))
x = simulate_celular_latency(0.069, 1.01)
print(round(x,2))
x = simulate_celular_latency(0.069, 1.01)
print(round(x,2))


# fig.subplot(212)
# fig.hist(aleat, bins=10)

plt.show()




# 0.0690