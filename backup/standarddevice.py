
from twisted.internet import protocol, reactor, endpoints
from twisted.python import log
import tkinter
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.networkcomponent import StandardClientNetworkComponent
import uuid
import time
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.endpoints import connectProtocol
from core.iconsRegister import getIconFileName
from core.functions import import_and_instantiate_class_from_string
from fabric.api import local
from bresenham import bresenham

class StandardServerDevice(object):
    
    def __init__(self, simulation_core, port, real_ip, name, icon, is_wireless, x, y, application, coverage_area_radius):

        self.application = import_and_instantiate_class_from_string(application)
        self.addr = real_ip
        self.port = port
        
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]

        self.simulation_core = simulation_core
        self.name = name
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing Server")
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless

        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        self.application.start(self.addr, self.port)
        

    def confirure_network_link(self, link, transmission_rate, latency, packet_loss, network_interface):
        log.msg(f"Configuring the {link} to the serve on port {self.port} using {network_interface} interface")
        local(f"sudo tc qdisc replace dev {network_interface} root handle 1: prio priomap 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0")
        local(f"sudo tc qdisc replace dev {network_interface} parent 1:2 handle 20: netem delay {latency} rate {transmission_rate} loss {packet_loss} distribution pareto")
        local(f"sudo tc filter replace dev {network_interface} parent 1:0 protocol ip u32 match ip dport {self.port} 0xffff flowid 1:2")


class StandardClientDevice(object):
    
    def __init__(self, simulation_core, real_ip, name, icon, is_wireless, x, y, application, coverage_area_radius):

        self.application = import_and_instantiate_class_from_string(application)
        self.addr = real_ip

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]

        self.simulation_core = simulation_core
        self.name = name
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing Client")
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        self.network_component = StandardClientNetworkComponent(self.application)
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        


# ||||||||||||||||||||||| ROUTER ||||||||||||||||||||||||

class Router(object):

    def __init__(self, simulation_core, port, real_ip, name, icon, is_wireless, x, y, application, coverage_area_radius):
        
        self.application = import_and_instantiate_class_from_string(application)
        self.addr = real_ip
        self.port = port
        self.simulation_core = simulation_core
        self.name = name
        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.x = x
        self. y = y
        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing Router")

        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core

    def run(self):

        self.application.start(self.addr, self.port)

# ||||||||||||||||||||||| END ROUTER |||||||||||||||||||||||


# ||||||||||||||||||||||| WIRELESS DEVICE ||||||||||||||||||

#this is only for wsn - Rafael Sampaio
class WirelessDevice(object):
    def __init__(self):
        pass
    
    def find_nearby_devices_icon(self): 
        # getting all canvas objects in wifi signal coverage area - Rafael Sampaio
        all_coveraged_devices = self.simulation_core.canvas.find_overlapping(
                                                                            self.visual_component.x+self.coverage_area_radius,
                                                                            self.visual_component.y+self.coverage_area_radius,
                                                                            self.visual_component.x-self.coverage_area_radius,
                                                                            self.visual_component.y-self.coverage_area_radius)
        return all_coveraged_devices

    def get_nearby_devices_list(self):
        all_nearby_device = set()
        # putting all nearby devices icons in a list that will be use in future to send data across - Rafael Sampaio
        nearby_devices_icon_list = self.find_nearby_devices_icon()

        for icon_id in nearby_devices_icon_list:
           device = self.WSN_network_group.get_wsn_device_by_icon(icon_id)

           if device != None:
            all_nearby_device.add(device)

        return all_nearby_device

# ||||||||||||||||||| END WIRELESS DEVICE  ||||||||||||||||||



# |||||||||||||||||||||||| CONNECTION  ||||||||||||||||||||||

class Connection(object):

    def __init__(self, simulation_core, source_protocol, destiny_addr, destiny_port):
        self.simulation_core = simulation_core
        self.device1 = source_protocol
        self.device2 = simulation_core.get_any_protocol_by_addr_and_port(destiny_addr, destiny_port)
        
        if self.device1 and self.device2:
            self.create_connection(self.simulation_core, self.device1, self.device2)

    def create_connection(self,simulation_core, device1,device2):
        x1 = self.device1.visual_component.x
        y1 = self.device1.visual_component.y
        x2 = self.device2.visual_component.x
        y2 = self.device2.visual_component.y
        self.id = self.simulation_core.canvas.create_line(x1,y1,x2,y2,arrow="both", width=1, dash=(4,2))
        
        # The follow line was commented be cause it makes a recursive call wich crashes the tcp conection - Rafael Sampaio
        # self.simulation_core.canvas.after(10, self.update_connection_arrow, None)

        self.ball = self.simulation_core.canvas.create_oval(x1, y1, x1+7, y1+7, fill="red")
        self.all_coordinates = list(bresenham(x1, y1, x2,y2))
        self.display_time = 9 # time that the packege ball still on the screen after get the destinantion - Rafael Sampaio
        self.package_speed = 1 # this must be interger and determines the velocity of the packet moving in the canvas - Rafael Sampaio

        self.animate_package(x2,y2)


    def animate_package(self, destiny_x, destiny_y):
        cont = 100
        for x, y in self.all_coordinates:
            # verify if package ball just got its destiny - Rafael Sampaio
            if x == destiny_x and y == destiny_y:
                self.simulation_core.canvas.after(cont+self.display_time,self.simulation_core.canvas.delete, self.ball)

            self.simulation_core.canvas.after(cont, self.simulation_core.canvas.coords, self.ball, x, y, x+7, y+7) # 7 is the package ball size - Rafael Sampaio
            cont = cont + self.package_speed


    def update_connection_arrow(self,event):
        self.simulation_core.canvas.delete(self.id)
        self.create_connection(self.simulation_core, self.device1, self.device2)

# ||||||||||||||||||||| END CONNECTION  |||||||||||||||||||


# |||||||||||||||||||||||||| WSN ||||||||||||||||||||||||||    

class WirelessSensorNetwork(object):
    
    def __init__(self, simulation_core, wireless_standard, network_layer_protocol, application_layer_protocol, latency):
        self.simulation_core = simulation_core
        self.sink_list = set()
        self.repeater_list = set()
        self.sensors_list = set()
        self.network_layer_protocol = network_layer_protocol
        self.application_layer_protocol = application_layer_protocol
        self.wireless_standard = wireless_standard
        self.latency = latency

    # By using this function user can find any device into the wsn using the if of the draggable image incon.
    # This id is generated by the tkinter canvas. - Rafael Sampaio
    def get_wsn_device_by_icon(self, icon_id): 
        try:
            founded_device = None
            
            for device in self.sensors_list:
                if device.visual_component.draggable_img == icon_id:
                    founded_device = device
            
            for device in self.sink_list:
                if device.visual_component.draggable_img == icon_id:
                    founded_device = device
                
            for device in self.repeater_list:
                if device.visual_component.draggable_img == icon_id:
                    founded_device = device

            if founded_device != None:
                return founded_device

        except Exception as e:
            pass


class WSNSensorNode(WirelessDevice):
       
    def __init__(self, simulation_core, id, name, icon, is_wireless, x, y, application, coverage_area_radius, WSN_network_group):

        self.application = import_and_instantiate_class_from_string(application)
        self.WSN_network_group =  WSN_network_group
        self.is_wireless = is_wireless
        self.coverage_area_radius = coverage_area_radius
       
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.name = name+'_'+str(id)
        self.simulation_core = simulation_core

        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing sensor node")
        self.application.visual_component = self.visual_component
        self.application.visual_component.coverage_area_radius = coverage_area_radius
        self.application.simulation_core = self.simulation_core
        self.application.coverage_area_radius = coverage_area_radius
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))
    
    def run(self):
        
        nearby_devices_list = self.get_nearby_devices_list()
        self.application.start(nearby_devices_list)



class WSNRepeaterNode(WirelessDevice):
       
    def __init__(self, simulation_core, id, name, icon, is_wireless, x, y, application, coverage_area_radius, WSN_network_group):

        self.application = import_and_instantiate_class_from_string(application)
        self.WSN_network_group =  WSN_network_group
        self.is_wireless = is_wireless
        self.coverage_area_radius = coverage_area_radius
       
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.name = name+'_'+str(id)
        self.simulation_core = simulation_core

        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing repeater node")
        self.application.visual_component = self.visual_component
        self.application.visual_component.coverage_area_radius = coverage_area_radius
        self.application.simulation_core = self.simulation_core
        self.application.coverage_area_radius = coverage_area_radius
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))
    
    def run(self):
        
        nearby_devices_list = self.get_nearby_devices_list()
        self.application.start(nearby_devices_list)



class WSNSinkNode(WirelessDevice):
       
    def __init__(self, simulation_core, id, name, icon, is_wireless, x, y, application, coverage_area_radius, WSN_network_group):

        self.application = import_and_instantiate_class_from_string(application)
        self.WSN_network_group =  WSN_network_group
        self.is_wireless = is_wireless
        self.coverage_area_radius = coverage_area_radius

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.name = name
        self.id = id
        self.simulation_core = simulation_core

        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing sink node")
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))

    def run(self):
        nearby_devices_list = self.get_nearby_devices_list()
        self.application.start(nearby_devices_list)

# |||||||||||||||||||||||||| END WSN |||||||||||||||||||||||||| 


# |||||||||||||||||||||||| ACCESS POINT  ||||||||||||||||||||||

class AccessPoint(object):
    
    def __init__(self, simulation_core,  base_device, TBTT, SSID, WPA2_password, icon, is_wireless, x, y, application, coverage_area_radius):

        # self.base_device = base_device
        self.application = import_and_instantiate_class_from_string(application)
        # self.application.base_device = self.base_device
        
        # Target Beacon Transmission Time - Defines the interval to access point send beacon message. - Rafael Sampaio
        # IEEE standars defines default TBTT 100 TU = 102,00 mc = 102,4 ms = 0.01024 s. - Rafael Sampaio
        self.TBTT = TBTT or 0.3 #0.1024

        # SSID maximum size is 32 characters. - Rafael Sampaio
        self.SSID = SSID
        self.name = self.SSID
        self.WPA2_password = WPA2_password
        self.is_wireless = is_wireless
        self.coverage_area_radius = coverage_area_radius

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        
        self.simulation_core = simulation_core
        self.visual_component = VisualComponent(True, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.authenticated_devices = []
        self.associated_devices = []
        
        self.visual_component.set_coverage_area_radius(self.coverage_area_radius)

        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless
        self.application.TBTT = self.TBTT
        self.application.coverage_area_radius = coverage_area_radius
        self.application.gateway_addr = base_device.addr
        self.application.gateway_port = base_device.port


        self.simulation_core.updateEventsCounter("Initializing Access Point")
     
    def run(self):
        self.application.start()
    
# |||||||||||||||||||||||| END ACCESS POINT  ||||||||||||||||||||||


# |||||||||||||||||||||||| WIRELESS COMPUTER  |||||||||||||||||||||

class WirelessComputer(object):
       
    def __init__(self, simulation_core, name, icon, is_wireless, x, y, application, coverage_area_radius):

        self.application = import_and_instantiate_class_from_string(application)
        self.is_wireless = is_wireless
        self.coverage_area_radius = coverage_area_radius
       
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        self.name = name
        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        self.simulation_core = simulation_core

        self.is_wireless = is_wireless
        self.visual_component = VisualComponent(self.is_wireless, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.simulation_core.updateEventsCounter("Initializing wireless computer")
        self.application.visual_component = self.visual_component
        self.application.visual_component.coverage_area_radius = coverage_area_radius
        self.application.simulation_core = self.simulation_core
        self.application.coverage_area_radius = coverage_area_radius
        
        if(self.is_wireless == True):
            # setting image tag as "wifi_device" it will be useful when we need to verify if one device under wireless signal can connect to that. - Rafael Sampaio 
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_img, tags=("wifi_device",))
    
    def run(self):
        self.application.start()

# |||||||||||||||||||||||| END WIRELESS COMPUTER  |||||||||||||||||



################################# old codes section ################################

class AccessPoint_old(object):
    
    def __init__(self, simulation_core, port, real_ip, TBTT, SSID, WPA2_password, icon, is_wireless, x, y, application, router_addr, router_port, coverage_area_radius):

        self.application = import_and_instantiate_class_from_string(application)
        
        # Target Beacon Transmission Time - Defines the interval to access point send beacon message. - Rafael Sampaio
        # IEEE standars defines default TBTT 100 TU = 102,00 mc = 102,4 ms = 0.01024 s. - Rafael Sampaio
        self.TBTT = TBTT or 0.3 #0.1024
        self.addr = real_ip
        self.port = port

        # SSID maximum size is 32 characters. - Rafael Sampaio
        self.SSID = SSID
        self.name = self.SSID
        self.WPA2_password = WPA2_password
        self.is_wireless = is_wireless

        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file

        # generating an unic id for the instance object. - Rafael Sampaio.
        self.id = uuid.uuid4().fields[-1]
        
        self.simulation_core = simulation_core
        self.visual_component = VisualComponent(True, self.simulation_core, self.name, self.icon, x, y, coverage_area_radius, self)
        self.authenticated_devices = []
        self.associated_devices = []
        
        self.visual_component.set_coverage_area_radius(200)

        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless
        self.application.TBTT = self.TBTT
        self.application.router_addr = router_addr
        self.application.router_port = router_port

        self.simulation_core.updateEventsCounter("Initializing Access Point")
     
    def run(self):
        self.application.start(self.addr, self.port)

