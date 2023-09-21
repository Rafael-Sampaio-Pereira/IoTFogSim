from apps.base_app import BaseApp
from twisted.internet import reactor
import datetime
from apps.smart_traits.temperature_control import TemperatureControl


class ShowerApp(BaseApp):
    def __init__(self):
        super(ShowerApp, self).__init__()
        self.name = 'ShowerApp'
        self.temperature_control = TemperatureControl(24.0, 50.0, 39.1)

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (watts); temperature (°C); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{str(self.temperature_control.temperature)};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())