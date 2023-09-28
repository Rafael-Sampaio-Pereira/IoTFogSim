import datetime
import random
from apps.base_app import BaseApp
from twisted.internet import reactor
from apps.smart_traits.fan_speed import FanSpeed


class VentilatorApp(BaseApp):
    def __init__(self):
        super(VentilatorApp, self).__init__()
        self.name = 'VentilatorApp'
        self.fan_speed = FanSpeed(30)
    
    def set_fan_speed(self, fan_speed=None):
        if self.machine.is_turned_on:
            self.fan_speed.fan_speed_percent = fan_speed or random.randint(0,3)
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} fan speed: {self.fan_speed.fan_speed_percent}")

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (Kw); fan speed; last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{str(self.fan_speed.fan_speed_percent) if self.machine.is_turned_on else '-'};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())