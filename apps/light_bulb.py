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
        LoopingCall(self.update_dataset).start(interval=1, now=True)


# Generic sensor
#    |-- Generic Float Sensor
#    |-- Generic Int Sensor 
#    |-- Generic Binary Sensor

# dispositivos salvar tensão/ corrente e potencia por segundo

# arcondicionado temperatura