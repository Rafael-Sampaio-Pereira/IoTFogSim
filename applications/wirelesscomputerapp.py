
from twisted.internet import reactor
import time
import uuid
import tkinter as tk

from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.task import LoopingCall




class WirelessComputerApp(StandardApplicationComponent):
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.associated_ap = None
        self.is_connected = False
    
    def start(self):
        self.source_addr = '127.0.0.1'
        self.source_port = '8888'
        self.destiny_addr = '127.0.0.1'
        self.destiny_port = '8082'
        main = LoopingCall(self.main_app)
        main.start(0.1)  # run your own loop 10 times a second

    def main_app(self):
        # this function is the main app running in the computer - Rafael Sampaio
        # any application or network protocol can be implemented here - Rafael Sampaio

        self.is_connected = self.verify_wireless_connection()

        if self.is_connected:
            # Creating a http package - Rafael Sampaio
            payload = 'HTTP 1.0 / GET request'
            package = self.build_package(payload)
            self.send(package)

            
            # FALTA:
            #     - COLOCAR PACOTE NO BUFFER DO access point
            #     - PASSAR DO AP PARA ROUTER
            #     - CRIAR FLAG NA HORA Q O DADO FOR PASSADO DO AP PARA O ROUTER INDICADO QUE O DADO DEVE SER DEVOLVIDO
            #         AO AP E O AP DEVE TER UMA MANEIRA DE IDENTIFICAR OS DISPOSITIVOS CONECTADOS E ENTREGAR A ELES
        else:
            print('Not connected to a wireless access point')

    # this method is overhidding the send method in StandardApplicationComponent class - Rafael Sampaio
    def send(self, package):
        # puting package in the access point buffer - Rafael Sampaio
        self.associated_ap._buffer.add(package)



    def verify_wireless_connection(self):
        # verifying if this device is connected to access point - Rafael Sampaio
        if self.associated_ap:
            return True
        else:
            return False
        




        
        # # for each nearby device we need to build a diferent package, but the content (payload) can be same - Rafael Sampaio
            
        # for device in self.nearby_devices_list:
        #     # Creating a new package - Rafael Sampaio
        #     pack = WSNPackage(self, device, data)

        #     # putting this device in the generated package trace - Rafael Sampaio
        #     pack.put_in_trace(self)

        #     # putting data in device buffer - Rafael Sampaio
        #     self._buffer.add(pack) 

        # #self.print_node_buffer()

        # def remove_sent_packages_from_buffer(_package):
        #     # after send, remove data from buffer - Rafael Sampaio    
        #     self._buffer.remove(_package)

        # if len(self._buffer) > 0:
        #     self.temp_buffer = self._buffer.copy()
            
        #     # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
        #     for _package in self.temp_buffer:
        #         self.forward_package(_package)
                
        #         self.simulation_core.canvas.after(5, remove_sent_packages_from_buffer, _package)
                
    
        # reactor.callLater(self.interval, self.collect_and_send_data)

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

