import random
from core.simulationcore import SimulationCore

class ColorSetting(object):
    """https://developers.home.google.com/cloud-to-cloud/traits/colorsetting?hl=pt-br#pt-br"""
    
    def __init__(self,
                simulation_core: SimulationCore,
                color_model: str,
                temperature_min_kelvin: int,
                temperature_max_kelvin: int,
                rgb: tuple,
                hsv: tuple
        ):
        self.color_model: str = color_model if color_model in ['rgb', 'hsv'] else 'rgb'
        self.rgb: tuple = rgb
        self.hsv: tuple = hsv
        self.simulation_core: SimulationCore = simulation_core
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        self.temperature_kelvin: int = random.uniform(
            temperature_min_kelvin,
            temperature_max_kelvin
        )