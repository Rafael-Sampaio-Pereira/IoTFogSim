
from twisted.internet import protocol, reactor, endpoints
from twisted.python import log
import tkinter
from config.settings import ICONS_PATH
from scinetsim.visualcomponent import VisualComponent
from scinetsim.networkcomponent import StandardServerNetworkComponent
from scinetsim.networkcomponent import StandardClientNetworkComponent
import uuid

class StandardServerDevice(object):
    
    def __init__(self, canvas):
        self.access_point = None
        self.real_ip = None
        self.simulation_ip = "192.121.0.1"

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        self.canvas = canvas
        self.name = "Server - %s"%(self.simulation_ip)
        self.visual_component = VisualComponent(False, self.canvas, self.name, ICONS_PATH+"scinetsim_restfull_server.png", 100, 100)
        self.network_component = StandardServerNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)

    def run(self):
        endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)


class StandardClientDevice(object):
    
    def __init__(self, canvas):
        self.access_point = None
        self.real_ip = None
        self.simulation_ip = "192.121.0.1"

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        self.canvas = canvas
        self.name = "Client - %s"%(self.simulation_ip)
        self.visual_component = VisualComponent(True, self.canvas, self.name, ICONS_PATH+"scinetsim_esp8266.png", 100, 100)
        self.network_component = StandardClientNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)
        
        # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
        self.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        

class AccessPoint(object):

    def __init__(self, canvas):
        
        # Target Beacon Transmission Time - Defines the interval to access point send beacon message. - Rafael Sampaio
        # IEEE standars defines default TBTT 100 TU = 102,00 mc = 102,4 ms = 0.01024 s. - Rafael Sampaio
        self.TBTT = 0.1024

        # SSID maximum size is 32 characters. - Rafael Sampaio
        self.SSID = "Access_Point"
        self.name = self.SSID
        self.WPA2_password = "scinetsim2019"

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        self.canvas = canvas
        self.visual_component = VisualComponent(True, self.canvas, self.name, ICONS_PATH+"scinetsim_access_point.png", 100, 100)
        self.authenticated_devices = []
        self.associated_devices = []
        
        # This stores the twisted protocol instance for the router device. - Rafael Sampaio
        self.router_protocol = None
        self.visual_component.set_coverage_area_radius(200)
        
        # Sends beacon frame. - Rafael Sampaio
        self.passive_scanning()
        

    def run(self):
        pass
        #endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)

    # when the wifi access point executes the passive scanning metho, it is sending an beacon frame(in broadcast mode) for every device around it. - Rafael Sampaio
    def passive_scanning(self):
        
        #log.msg("%s - Sending Wifi 802.11/* beacon broadcast message..."%(self.SSID))
        self.canvas.itemconfig(self.visual_component.draggable_alert, fill="red")
        self.canvas.itemconfig(self.visual_component.draggable_alert, text="<< beacon >>")

        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        
        # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
        if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
            # the ssignal radius propagates at 10 units per time. - Rafael Sampaio
            self.visual_component.signal_radius += 10
            self.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            
            # getting all canvas objects in wifi signal coverage area
            all_coveraged_devices = self.canvas.find_overlapping(self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            

            # finding all the wifi devices on the canvas screen. - Rafael Sampaio
            wifi_devices = self.canvas.find_withtag("wifi_device")
            
            # Verifys if are device coveraged by the wifi signal and if the wifi devices list has any object. - Rafael Sampaio         
            if len(all_coveraged_devices) > 0 or len(wifi_devices) > 0:
                # for each device into wifi signal coverage area, verify if this is an wifi device, then run any action. - Rafael Sampaio
                for device in all_coveraged_devices:
                    if device in wifi_devices:
                        self.canvas.itemconfig(self.visual_component.draggable_alert, fill="green")
                        self.canvas.itemconfig(self.visual_component.draggable_alert, text="Found devices")
                        #pass
                        #log.msg(self.canvas.itemcget(device,"tags"))
                    else:
                        pass
                        #log.msg("The device is not wireless based")
            else:
                log.msg("There is no wifi devices in this simulation or it is not in this wifi signal coverage area.")

        else:
            # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
            self.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline = "")
            self.visual_component.signal_radius = 1

        self.canvas.update()
        # Reactor will send an beacon frame using passive scanning method at each TBTT interval time. - Rafael Sampaio
        reactor.callLater(self.TBTT, self.passive_scanning)