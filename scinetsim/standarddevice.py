
from twisted.internet import protocol, reactor, endpoints
from twisted.python import log
import tkinter
from config.settings import ICONS_PATH
from scinetsim.visualcomponent import VisualComponent
from scinetsim.networkcomponent import StandardClientNetworkComponent
import uuid
import time
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import connectProtocol
from scinetsim.iconsRegister import getIconFileName
from scinetsim.functions import import_and_instantiate_class_from_string

class StandardServerDevice(object):
    
    def __init__(self, simulation_core, port, real_ip, simulation_ip, id, name, icon, is_wireless, x, y, application):

        self.application = import_and_instantiate_class_from_string(application)
        self.addr = real_ip
        self.port = port
        self.simulation_ip = simulation_ip
        
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        #self.id = uuid.uuid4().fields[-1]

        self.id = id
        self.simulation_core = simulation_core
        self.name = name
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y)
        self.simulation_core.updateEventsCounter("Initializing Server")
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless

        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        self.application.start(self.addr, self.port)


class StandardClientDevice(object):
    
    def __init__(self, simulation_core, real_ip, simulation_ip, id, name, icon, is_wireless, x, y, application):
        self.addr = real_ip
        self.simulation_ip = simulation_ip

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        #self.id = uuid.uuid4().fields[-1]

        self.id = id
        self.simulation_core = simulation_core
        self.name = name
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y)
        self.network_component = StandardClientNetworkComponent(self.visual_component, self.simulation_core, application, is_wireless)
        self.simulation_core.updateEventsCounter("Initializing Client")
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        


class Router(object):

    def __init__(self, simulation_core, port, real_ip, simulation_ip, id,name, icon, is_wireless, x, y, application):
        
        self.application = import_and_instantiate_class_from_string(application)
        self.addr = real_ip
        self.port = port
        self.simulation_core = simulation_core
        
        self.simulation_ip = simulation_ip
        self.name = name
        # generating an unic id for the instance object. - Rafael Sampaio.
        #self.id = uuid.uuid4().fields[-1]

        self.id = id
        
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.x = x
        self. y = y
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y)
        self.simulation_core.updateEventsCounter("Initializing Router")

        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core

    def run(self):

        self.application.start(self.addr, self.port)


class AccessPoint(object):

    def __init__(self, simulation_core, simulation_ip, id, TBTT, SSID, WPA2_password, icon, is_wireless, x, y):
        
        # Target Beacon Transmission Time - Defines the interval to access point send beacon message. - Rafael Sampaio
        # IEEE standars defines default TBTT 100 TU = 102,00 mc = 102,4 ms = 0.01024 s. - Rafael Sampaio
        self.TBTT = TBTT or 0.1024
        self.simulation_ip = simulation_ip

        # SSID maximum size is 32 characters. - Rafael Sampaio
        self.SSID = SSID
        self.name = self.SSID
        self.WPA2_password = WPA2_password
        self.is_wireless = is_wireless

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        #self.id = uuid.uuid4().fields[-1]

        self.id = id
        
        self.simulation_core = simulation_core
        self.visual_component = VisualComponent(True, self.simulation_core, self.name, self.icon, x, y)
        self.authenticated_devices = []
        self.associated_devices = []
        
        # This stores the twisted protocol instance for the router device. - Rafael Sampaio
        self.router_protocol = None
        self.visual_component.set_coverage_area_radius(200)

        self.simulation_core.updateEventsCounter("Initializing Access Point")
        
        # Sends beacon frame. - Rafael Sampaio
        self.passive_scanning()
        

    def run(self):
        pass

    # when the wifi access point executes the passive scanning metho, it is sending an beacon frame(in broadcast mode) for every device around it. - Rafael Sampaio
    def passive_scanning(self):
        
        self.simulation_core.updateEventsCounter("Access Point BEACON")

        #log.msg("%s - Sending Wifi 802.11/* beacon broadcast message..."%(self.SSID))
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="red")
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text="<< beacon >>")

        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        
        # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
        if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
            # the ssignal radius propagates at 10 units per time. - Rafael Sampaio
            self.visual_component.signal_radius += 10
            self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            
            # getting all canvas objects in wifi signal coverage area
            all_coveraged_devices = self.simulation_core.canvas.find_overlapping(self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            

            # finding all the wifi devices on the canvas screen. - Rafael Sampaio
            wifi_devices = self.simulation_core.canvas.find_withtag("wifi_device")
            
            # Verifys if are device coveraged by the wifi signal and if the wifi devices list has any object. - Rafael Sampaio         
            if len(all_coveraged_devices) > 0 or len(wifi_devices) > 0:
                # for each device into wifi signal coverage area, verify if this is an wifi device, then run any action. - Rafael Sampaio
                for device in all_coveraged_devices:
                    if device in wifi_devices:
                        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="green")
                        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text="Found devices")
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





class Connection(object):

    def __init__(self, simulation_core, source_protocol, destiny_addr, destiny_port):
        self.simulation_core = simulation_core
        self.device1 = source_protocol
        self.device2 = simulation_core.get_any_protocol_by_addr_and_port(destiny_addr, destiny_port)
        self.create_connection(self.simulation_core, self.device1, self.device2)

    def create_connection(self,simulation_core, device1,device2):
        x1 = self.device1.visual_component.x
        y1 = self.device1.visual_component.y
        x2 = self.device2.visual_component.x
        y2 = self.device2.visual_component.y
        self.id = self.simulation_core.canvas.create_line(x1,y1,x2,y2,arrow="both", width=1, dash=(4,2))
        self.simulation_core.canvas.after(10, self.update_connection_arrow, None)

    def update_connection_arrow(self,event):
        self.simulation_core.canvas.delete(self.id)
        self.create_connection(self.simulation_core, self.device1, self.device2)


        


