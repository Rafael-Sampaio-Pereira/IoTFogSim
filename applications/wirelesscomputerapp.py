
from twisted.internet import reactor
import time
import uuid
import tkinter as tk





class WirelessComputerApp(object):
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.associated_ap = None
    
    def start(self):
        pass
        #self.print_info()

    def print_info(self):
        print(self.associated_ap)
        reactor.callLater(3, self.print_info)


    def collect_and_send_data(self):
        
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
                
    
        reactor.callLater(self.interval, self.collect_and_send_data)

    def forward_package(self, package):
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
                            self.draw_connection_arrow(destiny)

                            # puting package in destiny device buffer - Rafael Sampaio
                            destiny.application._buffer.add(package)
                            
                            package.put_in_trace(destiny)
                            #package.print_trace()

                            self.simulation_core.updateEventsCounter("wsn node send data")

