
from twisted.internet import protocol, reactor, endpoints
from twisted.python import log
import tkinter
from config.settings import ICONS_PATH
from scinetsim.visualcomponent import VisualComponent
from scinetsim.networkcomponent import StandardServerNetworkComponent
from scinetsim.networkcomponent import StandardClientNetworkComponent


class StandardServerDevice(object):
    
    def __init__(self, canvas):
        self.real_ip = None
        self.simulation_ip = "192.121.0.1"
        self.canvas = canvas
        self.name = "Server - %s"%(self.simulation_ip)
        self.visual_component = VisualComponent(False, self.canvas, self.name, ICONS_PATH+"scinetsim_restfull_server.png", 100, 100)

        self.network_component = StandardServerNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)

    def run(self):
        endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)


class StandardClientDevice(object):
    
    def __init__(self, canvas):
        self.real_ip = None
        self.simulation_ip = "192.121.0.1"
        self.canvas = canvas
        self.name = "Client - %s"%(self.simulation_ip)
        self.visual_component = VisualComponent(True, self.canvas, self.name, ICONS_PATH+"scinetsim_esp8266.png", 100, 100)
        self.network_component = StandardClientNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)

    def run(self):
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        

class AccessPoint(object):

    def __init__(self, canvas):
        # Target Beacon Transmission Time - Defines the interval to access point send beacon message. - Rafael Sampaio
        self.TBTT = 1
        self.SSID = "scinetsim_wifi_access_point"
        self.WAP2_password = "scinetsim2019"
        self.canvas = canvas
        self.name = self.SSID
        self.visual_component = VisualComponent(True, self.canvas, self.name, ICONS_PATH+"scinetsim_access_point.png", 100, 100)
        self.authenticated_devices = []
        self.associated_devices = []
        
        # This stores the twisted protocol instance for the router device. - Rafael Sampaio
        self.router_protocol = None
        self.sendBeacon()
        

    def sendBeacon(self):
        log.msg("%s - Sending Wifi 802.11/* beacon broadcast message..."%(self.SSID))
        self.canvas.itemconfig(self.visual_component.draggable_alert, text="beacon")
        self.visual_component.propagate_signal()
        reactor.callLater(self.TBTT, self.sendBeacon)
        

    def run(self):
        pass
        #endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)
