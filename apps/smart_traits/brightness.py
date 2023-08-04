

class Brightness(object):
    
    def __init__(self, initial_percentage: int):
        self.brightness: int = initial_percentage
        
    def set_brightness_percentage(self, new_percentage: int):
        self.brightness = new_percentage