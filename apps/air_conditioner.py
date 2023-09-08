from apps.base_app import BaseApp
from apps.smart_traits.fan_speed import FanSpeed
from apps.smart_traits.temperature_setting import TemperatureSetting


class AirConditionerApp(BaseApp):
    def __init__(self):
        super(AirConditionerApp, self).__init__()
        self.name = 'AirConditionerApp'
        self.fan_speed = FanSpeed(30)
        self.temperature_setting = TemperatureSetting(16.0, 24.0)