

class FanSpeed(object):
    
    def __init__(self, initial_percent: int):
        self.fan_speed_percent: int = initial_percent
        
    def set_fan_speed_percent(self, new_percent: int):
        self.fan_speed_percent = new_percent