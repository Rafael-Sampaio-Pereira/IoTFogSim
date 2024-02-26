import random

def simulate_power_consumption():
        """ This simulates power consumption considering power variance.
        To call it, you need to use a variance margin(float_margin) value"""
        min_power = None
        power_watts = 1500
        power_float_margin = 0.7
        if power_watts - power_float_margin < 1:
            min_power = power_watts
        else:
            min_power = power_watts - power_float_margin
            
        max_power = power_watts+power_float_margin
        final_value = random.uniform(min_power, max_power)

        # print(f"name: {self.name}, original: {power_watts}, max: {max_power}, min: {min_power}, final: {final_value}")

        return final_value
    
    
    
for i in range(0,100):
    print(round(simulate_power_consumption()/1000,3))