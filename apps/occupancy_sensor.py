from apps.base_app import BaseApp
from twisted.internet import reactor
import datetime
from apps.smart_traits.occupancy_sensing import OccupancySensing


class OccupancySensorApp(BaseApp):
    def __init__(self):
        super(OccupancySensorApp, self).__init__()
        self.name = 'OccupancySensorApp'
        self.occupancy_sensing = OccupancySensing()
        self.environment = None

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consuption (watts); enviroment; occupancy; last actor'
            print(dataset_csv_header, file=self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.environment.name if self.environment else 'N/A'};"+\
            f"{self.occupancy_sensing.occupancy};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())