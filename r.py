import random

all = []

def power_consuption(power, float_margin):
    """ This simulates power consumption considering power variance.
    To call it, you need to use a variance margin(float_margin) value"""
    min_power = None
    if power - float_margin < 1:
        min_power = power
    else:
        min_power = power - float_margin
        
    max_power = power+float_margin
    return round(random.uniform(min_power, max_power),2)
    

for i in range(1, 10):
    pw = power_consuption(50, 5)
    print(pw)
    all.append(pw)
    
    
print(max(all), min(all))
