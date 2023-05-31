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
        dataset_csv_header = 'power consuption watts'
        print(dataset_csv_header, file = self.dataset_file, flush=True)
        LoopingCall(
            self.update_dataset,
            'teste'
        ).start(self.simulation_core.clock.get_internal_time_unit(1))
