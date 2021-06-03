
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import connectProtocol
import tkinter as tk
from twisted.python import log

from bresenham import bresenham


# this protocol acts as a client to the router/switch - Rafael Sampaio
class AccessPointAppProtocol(StandardApplicationComponent):
    
    def __init__(self, simulation_core, visual_component):
        self.visual_component = visual_component
        self.simulation_core =  simulation_core
        self._out_buffer = set()

    def connectionMade(self):
        self.transport.setTcpKeepAlive(1)
        self.terminateLater = None
        self.create_connection_animation()

    # This method is overhidding the dataReceived method in the StandardApplicationComponent class - Rafael Sampaio
    def dataReceived(self, data):
        self.put_package_in_buffer(data)

    def connectionLost(self, reason):
        pass     
         
    def write(self, data):
        if data:
            self.transport.write(data)

    # This method is overhidding the put_package_in_buffer method in the StandardApplicationComponent class - Rafael Sampaio
    def put_package_in_buffer(self, data):
        if data.endswith(b"\n"):
            packages = data.split(b"\n")
            for package in packages:
                if package != b'':
                    self._out_buffer.add(package)


class AccessPointAppFactory(ClientFactory):

    def __init__(self, simulation_core, visual_component):
        self.running_protocol = None
        self.visual_component = visual_component
        self.simulation_core =  simulation_core

    def buildProtocol(self, address):
        self.running_protocol = AccessPointAppProtocol(self.simulation_core, self.visual_component)
        self.running_protocol.save_protocol_in_simulation_core(self.running_protocol) 
        return self.running_protocol



class AccessPointApp(StandardApplicationComponent):

    protocol.ClientFactory.noisy = False
    TCP4ClientEndpoint.noisy = False
        
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.coverage_area_radius = None
        self.TBTT = None
        self._in_buffer = set() # stores packages received from wifi devices - Rafael Sampaio
        # self._out_buffer = set() # stores packages received from gateway(router/switch) - Rafael Sampaio
        self.associated_devices = set()
        self.gateway_addr = '127.0.0.1'
        self.gateway_port = 8081
        self.ap_factory = None # this stores the factory used to connect to the gateway(router/switch) - Rafael Sampaio

    def start(self):
        self.connect_to_gateway()
        self.passive_scanning()
        self.forward_packages()

    # when the wifi access point executes the passive scanning metho, it is sending an beacon frame(in broadcast mode) for every device around it. - Rafael Sampaio
    def passive_scanning(self):
        
        #self.simulation_core.updateEventsCounter("Access Point BEACON")

        #log.msg("%s - Sending Wifi 802.11/* beacon broadcast message..."%(self.SSID))
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="red")
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text="<< beacon >>")

        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        
        # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
        if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
            # the ssignal radius propagates at 10 units per time. - Rafael Sampaio
            self.visual_component.signal_radius += 33
            self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            
            # getting all canvas objects in wifi signal coverage area - Rafael Sampaio
            all_coveraged_devices = self.simulation_core.canvas.find_overlapping(self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            

            # finding all the wifi devices on the canvas screen. - Rafael Sampaio
            wifi_devices = self.simulation_core.canvas.find_withtag("wifi_device")
            
            # Verifys if are device coveraged by the wifi signal and if the wifi devices list has any object. - Rafael Sampaio         
            if len(all_coveraged_devices) > 0 and len(wifi_devices) > 0:
                # for each device into wifi signal coverage area, verify if this is an wifi device, then run any action. - Rafael Sampaio
                for device_icon in all_coveraged_devices:
                    # print(device_icon)
                    if device_icon in wifi_devices:
                        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="green")
                        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text="Found devices")
                        device = self.get_device_by_icon(device_icon)
                        
                        if device:
                            self.associate(device)
                    else:
                        pass
                        #log.msg("The device is not wireless based")
            else:
                log.msg("There is no wifi devices in this simulation or it is not in this wifi signal coverage area.")

        else:
            # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline = "")
            self.visual_component.signal_radius = 1

        self.simulation_core.canvas.update()
        # Reactor will send an beacon frame using passive scanning method at each TBTT interval time. - Rafael Sampaio
        reactor.callLater(self.TBTT, self.passive_scanning)

    def draw_connection_to_associated_device_arrow(self, device):
        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = device.visual_component.x
        y2 = device.visual_component.y
        connection_id = self.simulation_core.canvas.create_line(x1,y1,x2,y2, arrow="both", width=1, dash=(4,2))
        self.simulation_core.canvas.after(10, self.update_connection_to_associated_device_arrow, None, connection_id, device)

        


    def animate_package(self, destiny_x, destiny_y):
        cont = 100
        for x, y in self.all_coordinates:
            # verify if package ball just got its destiny - Rafael Sampaio
            if x == destiny_x and y == destiny_y:
                self.simulation_core.canvas.after(cont+self.display_time,self.simulation_core.canvas.delete, self.ball)

            self.simulation_core.canvas.after(cont, self.simulation_core.canvas.coords, self.ball, x, y, x+7, y+7) # 7 is the package ball size - Rafael Sampaio
            cont = cont + self.package_speed

    def update_connection_to_associated_device_arrow(self,event, id, device):
        self.simulation_core.canvas.delete(id)
        self.draw_connection_to_associated_device_arrow(device)


    def associate(self, device):
        # esta associação está sendo feita de forma simples e precisa ser melhorada, incluido passos como autenticação. - Rafael Sampaio
        if not (device in self.associated_devices) and device.application.is_connected == False:
            self.associated_devices.add(device)
            device.application.associated_ap = self
            device.application.is_connected = True
            self.draw_connection_to_associated_device_arrow(device)
            self.print_associated_devices()

            self.ball = self.simulation_core.canvas.create_oval(self.visual_component.x, self.visual_component.y, self.visual_component.x+7, self.visual_component.y+7, fill="red")
            self.all_coordinates = list(bresenham(self.visual_component.x, self.visual_component.y, device.visual_component.x, device.visual_component.y))
            self.display_time = 9 # time that the packege ball still on the screen after get the destinantion - Rafael Sampaio
            self.package_speed = 1 # this determines the velocity of the packet moving in the canvas - Rafael Sampaio

            self.animate_package(device.visual_component.x,device.visual_component.y)
            

    def get_device_by_icon(self, icon_id):
        try:
            founded_device = None
    
            for device in self.simulation_core.allNodes:
                if device.visual_component.draggable_img == icon_id:
                    founded_device = device

            if founded_device != None:
                return founded_device

        except Exception as e:
            pass

    def print_associated_devices(self):
        for device in self.associated_devices:
            print("Assossiated to :", device.name)
    
    def get_associated_device_by_addr_and_port(self, device_addr, device_port):
        if len(self.associated_devices) > 0:
            for device in self.associated_devices:
                if device.application.get_addr() == device_addr and device.application.get_port() == device_port:
                    return device


    def verify_in_buffer(self):
        if len(self._in_buffer) > 0:
            return True
        else:
            return False

    def verify_out_buffer(self):
        if self.ap_factory.running_protocol:
            if len(self.ap_factory.running_protocol._out_buffer) > 0:
                return True
            else:
                return False
        else:
            return False

    def forward_packages(self):
        if self.verify_in_buffer():
            if self.ap_factory.running_protocol:
                # forwarding packages to the router - Rafael Sampaio
                for package in self._in_buffer.copy():
                    # this uses the send method defined in the StandardApplicationComponent class - Rafael Sampaio
                    self.ap_factory.running_protocol.send(package)
                    self._in_buffer.remove(package)

        if self.verify_out_buffer():
            for package in self.ap_factory.running_protocol._out_buffer.copy():
                destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
                destiny_device = self.get_associated_device_by_addr_and_port(destiny_addr, destiny_port)
                if destiny_device:
                    destiny_device.application._buffer.add(package)
                    self.ap_factory.running_protocol._out_buffer.remove(package)
                
        reactor.callLater(1, self.forward_packages)


    # this method allow the access point to connect to router/switch - Rafael Sampaio
    def connect_to_gateway(self):

        # get start to connect to gateway - Rafael Sampaio
        factory = AccessPointAppFactory(self.simulation_core, self.visual_component)
        factory.noisy = False
        reactor.connectTCP(self.gateway_addr, self.gateway_port, factory)
        self.ap_factory = factory        

