

class FanSpeed(object):
    
    def __init__(self, fan_speed_percent: int):
        self.fan_speed_percent: int = fan_speed_percent
        
    def set_fan_speed(self, fan_speed_percent: int):
        self.fan_speed_percent = fan_speed_percent