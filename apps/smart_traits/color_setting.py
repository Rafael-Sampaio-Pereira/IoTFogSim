import random


class ColorSetting(object):
    """https://developers.home.google.com/cloud-to-cloud/traits/colorsetting?hl=pt-br#pt-br"""
    
    def __init__(self,
                color_model: str,
                temperature_min_kelvin: int,
                temperature_max_kelvin: int,
                rgb: tuple = (255, 255, 255), # Default White color
                hsv: tuple = (0, 0, 100) # Default White color
        ):
        self.color_model: str = color_model if color_model in ['rgb', 'hsv'] else 'rgb'
        self.rgb: tuple = rgb
        self.hsv: tuple = hsv
        self.temperature_kelvin: int = random.randint(
            temperature_min_kelvin,
            temperature_max_kelvin
        )