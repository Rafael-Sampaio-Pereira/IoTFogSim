import datetime
import random
from apps.base_app import BaseApp
from twisted.internet import reactor
from apps.smart_traits.cook import Cook
from apps.smart_traits.fan_speed import FanSpeed


class MicrowaveApp(BaseApp):
    def __init__(self):
        super(MicrowaveApp, self).__init__()
        self.name = 'MicrowaveApp'
        self.cook = Cook('BAKE')
    
    def set_cooking_mode(self, cooking_mode=None):
        if self.machine.is_turned_on:
            self.cook.cooking_mode = cooking_mode or random.choice(self.cook.valids_cooking_modes)
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} cooking mode: {self.cook.cooking_mode}")

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day;time;machine;status;power consumption (Kw);cook mode;last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{str(self.cook.cooking_mode) if self.machine.is_turned_on else '-'};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())