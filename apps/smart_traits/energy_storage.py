

class EnergyStorage(object):
    
    def __init__(self, initial_percent: int):
        self.capacity_initial: int = initial_percent
        self.capacity_remaning: int = initial_percent
        self.is_plugged_in: bool = False
        self.is_charging: bool = False
        self.initial_time: int = 0 # indicates the time in seconds
        
    def set_capacity_remaning(self, new_percent: int):
        self.capacity_remaning = new_percent
