import datetime
from apps.base_app import BaseApp
from twisted.internet.task import LoopingCall

class Light(object):
    def __init__(self):
        pass

class LightBulbApp(BaseApp, Light):
    def __init__(self):
        super(LightBulbApp, self).__init__()
        self.name = 'LightBulbApp'
        
        
        
    def main(self):
        super().main()
        dataset_csv_header = 'day; time; power consuption watts'
        print(dataset_csv_header, file = self.dataset_file, flush=True)
        LoopingCall(
            self.update_dataset,
            f"{self.simulation_core.clock.elapsed_days};"+
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+
            f"{round(self.machine.current_consumption,3)}"
        ).start(1)

# implementar sensor de humidade e temperatura interna
# torneira inelgigente pressão/vazão

# dispositivos salvar tensão/ corrente e potencia por segundo

# arcondicionado temperatura