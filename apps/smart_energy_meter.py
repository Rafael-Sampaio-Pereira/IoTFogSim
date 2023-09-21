
import datetime
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from apps.base_app import BaseApp
from components.machines import Machine


class SmartEnergyMeterApp(BaseApp):

    def __init__(self):
        super(SmartEnergyMeterApp, self).__init__()
        self.name ='Energy Meter'
        self.consumption_buffer = []
        self.total_consumption = 0

    def performe_mesures_per_second(self):
        temp_buffer = self.consumption_buffer.copy()
        mesure = 0
        if len(temp_buffer)>0:
            for ms in temp_buffer:
                mesure += ms
                self.total_consumption += ms
                self.consumption_buffer.remove(ms)
        return mesure


    def mesure_energy(self, value):
        self.consumption_buffer.append(value)

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (watts); mesured energy (watts); total mesured energy (watts); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.performe_mesures_per_second()};"+\
            f"{str(self.total_consumption)};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())