
from twisted.internet import reactor
import time
import uuid
import tkinter as tk
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.task import LoopingCall


# this class has atributes used to control the main app during loop execution - Rafael Sampaio
class AppControls(object):
    def __init__(self):
        self.is_first_request = True

class WirelessComputerApp(StandardApplicationComponent):
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.associated_ap = None
        self.is_connected = False
        self.controls = AppControls()

    def get_addr(self):
        return self.source_addr

    def get_port(self):
        return self.source_port
    
    def start(self):
        self.source_addr = '127.0.0.1'
        self.source_port = 8888
        self.destiny_addr = '127.0.0.1'
        self.destiny_port = 8080
        main = LoopingCall(self.main_app)
        # the client needs to wait a few seconds for the server start. If this not wait the connection arrow between router and server will not be draw.
        time.sleep(1)
        main.start(0.1)  # run your own loop 10 times a second

    def main_app(self):
        # this function is the main app running in the computer - Rafael Sampaio
        # any application or network protocol can be implemented here - Rafael Sampaio

        self.is_connected = self.verify_wireless_connection()

        if self.is_connected:
            if self.controls.is_first_request:
                # Creating a http package - Rafael Sampaio
                payload = 'HTTP 1.0 / GET request'
                package = self.build_package(payload, 'http')
                self.send(package)
                self.controls.is_first_request = False
        else:
            print('Not connected to a wireless access point')

        
        for package in self._buffer:
            _, _, _, _, _, payload = self.extract_package_contents(package)
            # Print the received data on the sreen.  - Rafael Sampaio
            self.update_alert_message_on_screen(payload)

    # this method is overhidding the send method in StandardApplicationComponent class - Rafael Sampaio
    def send(self, package):
        # puting package in the access point buffer - Rafael Sampaio
        self.associated_ap._in_buffer.add(package)

    def verify_wireless_connection(self):
        # verifying if this device is connected to access point - Rafael Sampaio
        if self.associated_ap:
            return True
        else:
            return False
