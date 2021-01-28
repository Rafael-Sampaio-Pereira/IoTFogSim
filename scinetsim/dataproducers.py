import random
from random import choices

def energy_consumption_meter():
    return str(round(random.uniform(2.5,22.5), 2))+" Kwh"

def distribution_secundary_voltage_fluctuation_meter():
    # poor voltages values in a 220v system(ANEEL, prodist 8) Are: (191 =< readed_value and readed_value < 202) or (231 < readed_value =< 233) - Rafael Sampaio
    # suitable voltages values in a 220v system(ANEEL, prodist 8) Are: (202 =< readed_value and readed_value =< 231) - Rafael Sampaio
    reference_voltage = 220.0
    suitable_and_poor_values = [

        190.0,
        190.1,
        190.2,
        190.3,
        190.4,
        190.5,
        190.6,
        190.7,
        190.8,
        190.9,

        210.0,
        210.1,
        210.2,
        210.3,
        210.4,
        210.5,
        210.6,
        210.7,
        210.8,
        210.9,

        220.1,
        220.2,
        220.3,
        220.4,
        220.5,
        220.6,
        220.7,
        220.8,
        220.9,

        230.0,
        230.1,
        230.2,
        230.3,
        230.4,
        230.5,
        230.6,
        230.7,
        230.8,
        230.9,

    ]

    # the population is composed by the reference voltage value and an random value from the suitable and poor values list - Rafael Sampaio 
    population = [reference_voltage, random.choice(suitable_and_poor_values)]

    # the reference voltage value has more probalblity than the random choiced value - Rafael Sampaio
    weights = [60, 40]
    readed_value = choices(population, weights, k=1)

    return str(readed_value[0])+"v"
