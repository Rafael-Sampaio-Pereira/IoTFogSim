import numpy as np


available_thermostat_modes =  [
    "off",
    "heat",
    "cool",
    "on",
    "heatcool",
    "auto",
    "fan-only",
    "purifier",
    "eco",
    "dry"
]

class TemperatureSetting(object):
    def __init__(
        self,
        min_threshold_celsius,
        max_threshold_celsius,
        thermostat_mode = 'cool'
    ):
        self.thermostat_mode = thermostat_mode
        self.thermostat_temperature_unit = '°C'
        self.thermostat_temperature_range = [ 
            temperature for temperature in np.arange(
                min_threshold_celsius,
                max_threshold_celsius,
                step=1
            )
        ]

    def thermostat_set_mode(self, thermostat_mode):
        if self.thermostat_mode in available_thermostat_modes:
            self.thermostat_mode = thermostat_mode