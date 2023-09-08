import numpy as np


class TemperatureControl(object):
    def __init__(
        self,
        min_threshold_celsius,
        max_threshold_celsius,
        temperature
    ):
        self.temperature_step_celsius = 5
        self.min_threshold_celsius = min_threshold_celsius
        self.max_threshold_celsius = max_threshold_celsius
        self.temperature_range = [ 
            temperature for temperature in np.arange(
                min_threshold_celsius,
                max_threshold_celsius,
                self.temperature_step_celsius
            )
        ]
        self.temperature = temperature
        
        self.temperature_unit_for_ux = '°C'

    def set_temperature(self, temperature) -> None:
        self.temperature = temperature
