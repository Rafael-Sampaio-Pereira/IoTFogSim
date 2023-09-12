import datetime
from apps.base_app import BaseApp
from twisted.internet.task import LoopingCall
from apps.smart_traits.brightness import Brightness
from apps.smart_traits.color_setting import ColorSetting
from twisted.internet import reactor

class Light(object):
    def __init__(self):
        pass

class LightBulbApp(BaseApp, Light):
    def __init__(self):
        super(LightBulbApp, self).__init__()
        self.name = 'LightBulbApp'
        self.brightness = Brightness(initial_percent=70)
        self.color_setting = ColorSetting(
            color_model = 'rgb',
            temperature_min_kelvin = 2000,
            temperature_max_kelvin = 9000
        )

    def main(self):
        super().main()
        LoopingCall(self.update_dataset).start(
            interval=self.simulation_core.clock.get_internal_time_unit(1), now=True)

    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consuption (watts); brightness(%); rgb; temperature(kelvin); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.brightness.brightness_percent if self.machine.is_turned_on else 0};"+\
            f"{self.color_setting.rgb if self.machine.is_turned_on else (0, 0, 0)};"+\
            f"{self.color_setting.temperature_kelvin if self.machine.is_turned_on else 0};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())


# Generic sensor
#    |-- Generic Float Sensor
#    |-- Generic Int Sensor 
#    |-- Generic Binary Sensor

# dispositivos salvar tensão/ corrente e potencia por segundo

# arcondicionado temperatura