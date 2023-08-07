

class Brightness(object):
    
    def __init__(self, initial_percent: int):
        self.brightness_percent: int = initial_percent
        
    def set_brightness_percent(self, new_percent: int):
        self.brightness_percent = new_percent