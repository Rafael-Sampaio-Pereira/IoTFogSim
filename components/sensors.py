import random
from twisted.internet.task import LoopingCall
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName
from config.settings import ICONS_PATH

class GenericSensor(object):
    def __init__(self, simulation_core, x, y):
        self.simulation_core = simulation_core
        self.name = 'Generic Sensor'
        self.current_collected_data = None
        self.is_wireless = True
        icon_file = getIconFileName('sensor_icon')
        self.icon = ICONS_PATH+icon_file
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, 0, self)
        LoopingCall(self.collect_data).start(self.simulation_core.clock.get_internal_time_unit(1))

    def collect_data(self, low=1, high=10):
        """Collect a new value from monitoring envirioment or object"""
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        self.current_collected_data = high-low
        
    def get_data(self):
        return self.current_collected_data
    

class GenericFloatSensor(GenericSensor):
    def __init__(self, simulation_core, x, y):
        super(GenericFloatSensor, self).__init__(simulation_core, x, y)
        self.simulation_core = simulation_core
        self.name = 'Generic Float Sensor'
        
    def collect_data(self, low=1, high=10):
        """Collect a new value from monitoring envirioment or object"""
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        self.current_collected_data = round(random.uniform(low, high),2)
        

class GenericIntSensor(GenericSensor):
    def __init__(self, simulation_core, x, y):
        super(GenericIntSensor, self).__init__(simulation_core, x, y)
        self.simulation_core = simulation_core
        self.name = 'Generic Int Sensor'
        
    def collect_data(self, low=1, high=10):
        """Collect a new value from monitoring envirioment or object"""
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        self.current_collected_data = random.randint(low, high)
        
class GenericBinarySensor(GenericSensor):
    def __init__(self, simulation_core, x, y):
        super(GenericBinarySensor, self).__init__(simulation_core, x, y)
        self.simulation_core = simulation_core
        self.name = 'Generic Int Sensor'
        
    def collect_data(self, low=1, high=10):
        """Collect a new value from monitoring envirioment or object"""
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        self.current_collected_data = random.choice([0,1])