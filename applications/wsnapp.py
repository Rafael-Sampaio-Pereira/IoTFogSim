
from scinetsim.dataproducers import *
from twisted.internet import reactor
import time

class SensorApp(object):
    def __init__(self):
        self._buffer = set()
        self.interval = 3
        self.all_nearby_devices = set()
    
    def start(self):
        # putting all nearby devices in a list that will be use in future to send data across - Rafael Sampaio
        self.find_nearby_devices()
        time.sleep(0.3)
        self.collect_and_send_data()

    def collect_and_send_data(self):
        # collecting data - Rafael Sampaio
        data = energy_consumption_meter()

        # putting data in device buffer - Rafael Sampaio
        self._buffer.add(data)
        
        print(self._buffer)

        # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
        for data in self._buffer.copy():
            self.send_via_broadcast(data)
            self._buffer.remove(data)
        
        reactor.callLater(self.interval, self.collect_and_send_data)
    
    def find_nearby_devices(self):
        # This function should only be called once, in the start method - Rafael Sampaio
        pass
    
    def send_via_broadcast(self, data):
        print(data)



class SinkApp(object):
    def __init__(self):
        pass