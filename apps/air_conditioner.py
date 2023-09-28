import datetime
import random
from apps.base_app import BaseApp
from twisted.internet import reactor
from apps.smart_traits.fan_speed import FanSpeed
from apps.smart_traits.temperature_setting import TemperatureSetting


class AirConditionerApp(BaseApp):
    def __init__(self):
        super(AirConditionerApp, self).__init__()
        self.name = 'AirConditionerApp'
        self.fan_speed = FanSpeed(30)
        self.temperature_setting = TemperatureSetting(16.0, 24.0)
    
    def set_fan_speed(self, fan_speed=None):
        if self.machine.is_turned_on:
            self.fan_speed.fan_speed_percent = fan_speed or random.randint(0,100)
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} fan speed: {self.fan_speed.fan_speed_percent}%")

    def set_temperature(self, temperature=None):
        if self.machine.is_turned_on:
            self.temperature_setting.temperature = temperature or random.uniform(16.0, 24.0)
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} temperature: {self.temperature_setting.temperature} °c")


    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (Kw); mode; temperature (°C); fan speed (%); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.temperature_setting.thermostat_mode if self.machine.is_turned_on else '-'};"+\
            f"{str(self.temperature_setting.thermostat_temperature_ambient) if self.machine.is_turned_on else '-'};"+\
            f"{str(self.fan_speed.fan_speed_percent) if self.machine.is_turned_on else '-'};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())