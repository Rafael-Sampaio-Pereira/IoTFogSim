

class EnergyStorage(object):
    
    def __init__(self, initial_percent: int):
        self.capacity_initial: int = initial_percent
        self.capacity_remaning: int = initial_percent
        self.is_plugged_in: bool = False
        self.is_charging: bool = False
        self.autonomy: int = 60 # indicates the time in seconds it takes to consume 1% of the total charge
        
    def set_capacity_remaning(self, new_percent: int):
        self.capacity_remaning = new_percent
