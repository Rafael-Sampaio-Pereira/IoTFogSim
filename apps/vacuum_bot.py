
from apps.base_app import BaseApp
import datetime
from apps.smart_traits.energy_storage import EnergyStorage
from mobility.random_walk_mobility import RandomWalkMobility
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

class VacuumBotApp(BaseApp):

    def __init__(self):
        super(VacuumBotApp, self).__init__()
        self.name = 'Vaccum Bot'
        self.is_moving = False
        self.energy_storage = EnergyStorage(95)
        self.mobility = None

    def main(self):
        super().main()
        if self.machine.is_turned_on:
            self.energy_storage.initial_time = self.machine.up_time
            self.run_mobility()
            LoopingCall(self.decrease_energy_storage).start(
                interval=self.simulation_core.clock.get_internal_time_unit(15), now=True)
            

    def run_mobility(self):
        if not self.is_moving:
            self.mobility = RandomWalkMobility(
                self.machine.visual_component,
                self.simulation_core,
                30
            )
            self.mobility.is_stopped = False
            self.is_moving = True

    def decrease_energy_storage(self):
        
        if self.machine.is_turned_on and not self.energy_storage.is_charging:
            if self.energy_storage.capacity_remaning > 0:
                self.energy_storage.capacity_remaning -= 1
                    
            else:
                self.mobility.is_stopped = True
                self.is_moving = False
                self.machine.is_turned_on = False


    def charge(self):
        if self.machine.is_turned_on and not self.energy_storage.is_charging:
            
            self.machine.is_turned_on = False
            self.energy_storage.is_charging = True
            for i in range(1, 100):
                self.energy_storage.capacity_remaning += 1

            if self.energy_storage.capacity_remaning >= 99:
                self.energy_storage.is_charging = False


    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consuption (watts); battery(%); position (x,y); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            state = None

            if self.energy_storage.is_charging:
                state = 'CHARGING'
            elif self.machine.is_turned_on:
                state= 'ON'
            else:
                state = 'OFF'

            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{state};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on and self.energy_storage.is_charging else 0};"+\
            f"{self.energy_storage.capacity_remaning};"+\
            f"{self.machine.visual_component.x, self.machine.visual_component.y};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())
        
        