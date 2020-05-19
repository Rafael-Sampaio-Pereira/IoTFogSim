
from scinetsim.dataproducers import *
from twisted.internet import reactor
import time

class SensorApp(object):
    def __init__(self):
        self._buffer = set()
        self.interval = 3
        self.simulation_core = None
        self.visual_component = None
    
    def start(self, nearby_devices_list):
        
        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.coverage_area_radius, self.visual_component.y+self.visual_component.coverage_area_radius, self.visual_component.x-self.visual_component.coverage_area_radius, self.visual_component.y-self.visual_component.coverage_area_radius)

        self.print_node_connections(nearby_devices_list)

        self.collect_and_send_data()

    def collect_and_send_data(self):
        # collecting data - Rafael Sampaio
        data = energy_consumption_meter()

        # putting data in device buffer - Rafael Sampaio
        self._buffer.add(data)

        # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
        for data in self._buffer.copy():
            self.send_via_broadcast(data)
            # after send, remove data from buffer - Rafael Sampaio
            self._buffer.remove(data)
            #print(self._buffer)
        
        reactor.callLater(self.interval, self.collect_and_send_data)

    def send_via_broadcast(self, data):
        #print(data)
        pass
    
    def print_node_connections(self, nearby_devices_list):
        self_name = self.simulation_core.canvas.itemcget(self.visual_component.draggable_name, 'text')
        print("=========", self_name ,"==========")
        if len(nearby_devices_list) > 0:
            for nearby_device in nearby_devices_list:
                device_name = self.simulation_core.canvas.itemcget(nearby_device.application.visual_component.draggable_name, 'text')
                if self_name != device_name:
                    print(self_name, ' <-------> ', device_name)    
        print("=============================")


class SinkApp(object):
    def __init__(self):
        pass