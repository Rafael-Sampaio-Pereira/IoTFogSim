
from scinetsim.dataproducers import *
from twisted.internet import reactor
import time
import uuid
import tkinter as tk



class WSNApp(object):
    def propagate_signal(self):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
        if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
            # the ssignal radius propagates at 10 units per time. - Rafael Sampaio
            self.visual_component.signal_radius += 10
            self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
        else:
            # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline = "")
            self.visual_component.signal_radius = 1
        
        reactor.callLater(0.1, self.propagate_signal)

    
    def print_node_connections(self, nearby_devices_list):
        self_name = self.simulation_core.canvas.itemcget(self.visual_component.draggable_name, 'text')
        print("=========", self_name ,"==========")
        if len(nearby_devices_list) > 0:
            for nearby_device in nearby_devices_list:
                device_name = self.simulation_core.canvas.itemcget(nearby_device.application.visual_component.draggable_name, 'text')
                if self_name != device_name:
                    print(self_name, ' <-------> ', device_name)    
        print("=============================")
        print('\n')

    def print_node_buffer(self):
        self_name = self.simulation_core.canvas.itemcget(self.visual_component.draggable_name, 'text')
        buffer_string = ''
        for package in self._buffer:
            buffer_string += '|'+str(package.payload)
        print(self_name, buffer_string)
        print('\n')

class SensorApp(WSNApp):
    def __init__(self):
        self._buffer = set()
        self.interval = 3
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None
    
    def start(self, nearby_devices_list):

        self.nearby_devices_list = nearby_devices_list
        self.propagate_signal()
        self.print_node_connections(nearby_devices_list)

        self.collect_and_send_data()


    def collect_and_send_data(self):
        
        # collecting data - Rafael Sampaio
        data = energy_consumption_meter()


        # for each nearby device we need to build a diferent package, but the content (payload) can be same - Rafael Sampaio
            
        for device in self.nearby_devices_list:
            # Creating a new package - Rafael Sampaio
            pack = WSNPackage(self, device, data)

            # putting this device in the generated package trace - Rafael Sampaio
            pack.put_in_trace(self)

            # putting data in device buffer - Rafael Sampaio
            self._buffer.add(pack) 

        #self.print_node_buffer()

        def remove_sent_packages_from_buffer(_package):
            # after send, remove data from buffer - Rafael Sampaio    
            self._buffer.remove(_package)

        if len(self._buffer) > 0:
            self.temp_buffer = self._buffer.copy()
            # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
            for _package in self.temp_buffer:
                self.forward_package(_package)


                self.simulation_core.canvas.after(5, remove_sent_packages_from_buffer, _package)
                
                #self._buffer.remove(_package)

            # def remove_sent_packages_from_buffer():
            #     # after send, remove data from buffer - Rafael Sampaio    
            #     self._buffer = self._buffer - self.temp_buffer

            # self.simulation_core.canvas.after(2, remove_sent_packages_from_buffer)
            
        
        
        reactor.callLater(self.interval, self.collect_and_send_data)

    def forward_package(self, package):
        #if not package.was_forwarded:
        if len(package.trace) > 0:

                for destiny in self.nearby_devices_list:
                    if destiny == package.source:
                        # A device can not sent data to it self - Rafael Sampaio
                        pass
                    elif package.verify_if_device_is_in_trace(destiny):
                        # The package will not be send to devices that already in the package trace - Rafael Sampaio
                        pass
                    else:
                        # Veryfing if the package already in the buffer (the nearby devices can send data back and its duplicates package in the buffer) - Rafael Sampaio
                        if not package in destiny.application._buffer:
                            # Drawing connection - Rafael Sampaio
                            package.draw_connection_arrow()

                            # puting package in destiny device buffer - Rafael Sampaio
                            destiny.application._buffer.add(package)
                            #package.was_forwarded = True
                            package.put_in_trace(destiny)
                            package.print_trace()
                            
    


    


class SinkApp(WSNApp):
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None
    
    def start(self, nearby_devices_list):
        self.propagate_signal()

class WSNPackage(object):
    
    def __init__(self, source, destiny, payload):
        self.id = uuid.uuid4().fields[-1]
        self.source = source
        self.destiny = destiny
        self.payload = payload
        #self.was_forwarded = False
        self.trace = set()



    def get_package_as_json(self):
        
        all_destiny_names = ''

        package = {
            id: self.id,
            source: self.source.name,
            destiny: destiny.name,
            payload: self.payload
        }

        package = json.dumps(package)

        return package

    def delete_connection_arrow(self, id):
        self.source.simulation_core.canvas.delete(id)

    def draw_connection_arrow(self):
        x1 = self.source.visual_component.x
        y1 = self.source.visual_component.y
        x2 = self.destiny.visual_component.x
        y2 = self.destiny.visual_component.y
        connection_id = self.source.simulation_core.canvas.create_line(x1,y1,x2,y2, arrow=tk.LAST, width=3, dash=(4,2))

        self.source.simulation_core.canvas.after(2, self.delete_connection_arrow, connection_id)

    def put_in_trace(self, device):
        device_name = self.source.simulation_core.canvas.itemcget(device.visual_component.draggable_name, 'text')
        self.trace.add(device_name)

    def verify_if_device_is_in_trace(self, device):
        device_name = self.source.simulation_core.canvas.itemcget(device.visual_component.draggable_name, 'text')
        if device_name in self.trace:
            return True
        else:
            return False

    def print_trace(self):
        src = self.source.simulation_core.canvas.itemcget(self.source.visual_component.draggable_name, 'text')
        trace_string = str(self.id)+": "+src
        
        for device in self.trace:
            if not device == src:
                trace_string += " - "+device
        
        print(trace_string)
