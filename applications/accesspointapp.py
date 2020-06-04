
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import connectProtocol
import tkinter as tk



class AccessPointApp_old:

    
    protocol.ClientFactory.noisy = False
    TCP4ClientEndpoint.noisy = False
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.ap_factory = None
        self.TBTT = None
        self.router_addr = None
        self.router_port = None

    def start(self, addr, port):

        # updating name on screen - Rafael Sampaio
        self.screen_name  = addr+":"+str(port)
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(self.screen_name))

        # get start to listen to connections(i.e. inputs) - Rafael Sampaio
        self.ap_factory = AccessPointFactory(self.visual_component, self.simulation_core)
        self.ap_factory.noisy = False
        self.ap_factory.protocol = AccessPointAppProtocol
        self.ap_factory.protocol.router_addr = self.router_addr
        self.ap_factory.protocol.router_port = self.router_port

        # starting the ap as server to wait for input connections connections - Rafael Sampaio
        endpoint = TCP4ServerEndpoint(reactor, port, interface=addr)
        endpoint.noisy = False
        listenStarting = endpoint.listen(self.ap_factory)

        def save_protocol(p):

            # create a simple connection just to start the factory listen_potocol - Rafael_sampaio
            endpoint = TCP4ClientEndpoint(reactor, addr, port)
            endpoint.noisy = False
            factory = ClientFactory()
            factory.noisy = False
            factory.protocol = protocol.Protocol
            whenConnected = endpoint.connect(factory)

            def cbConnected(connectedProtocol):
                self.ap_factory.listen_protocol.visual_component = self.ap_factory.visual_component
                self.ap_factory.listen_protocol.simulation_core = self.ap_factory.simulation_core
                self.simulation_core.allProtocols.add(self.ap_factory.listen_protocol)

            def ebConnectError(reason):
                print("Error while try to connect to the ap")

            whenConnected.addCallbacks(cbConnected, ebConnectError)
        
           
        # Sends beacon frame. - Rafael Sampaio
        self.passive_scanning()

        listenStarting.addCallback(save_protocol)

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


class AccessPointAppProtocol(StandardApplicationComponent):

    protocol.ClientFactory.noisy = False
    TCP4ClientEndpoint.noisy = False

    def __init__(self):
        self.buffer = None
        self.client = None
        self.visual_component = None
        self.simulation_core =  None
    
    def dataReceived(self, package):

        #print("OPACOTE É %s"%(package))

        # Extracting package contents - Rafael Sampaio
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)

        def save_protocol(proto):
            try:
                if self.simulation_core:
                    # saving the protocol used by the ap as out(i.e. endponit to connect to a destiny host and redirect package) - Rafael Sampaio
                    self.simulation_core.allProtocols.add(proto)
                    proto.create_connection_animation()
            except NameError:
                log.msg("The requested simulation_core is no longer available")

        # get start to connect redirect the receivede package - Rafael Sampaio
        factory = protocol.ClientFactory()
        factory.noisy = False
        cur_protocol = ClientProtocol()
        cur_protocol.noisy = False
        cur_protocol.visual_component = self.visual_component
        cur_protocol.simulation_core = self.simulation_core
        factory.protocol = cur_protocol
        cur_protocol.factory = factory
        factory.server = self
        
        # conncecting to destiny and aping received packages - Rafael Sampaio
        point = TCP4ClientEndpoint(reactor, self.router_addr, self.router_port)
        point.noisy = False
        d = connectProtocol(point, cur_protocol)
        # After connect, save the protocol - Rafael Sampaio
        d.addCallback(save_protocol)

        if self.client:
            self.client.write(package)
            self.client.transport.loseConnection()
        else:
            self.buffer = package

    def write(self, package):
        self.transport.write(package)
        

    def connectionMade(self):
        # saving the ap protocol that acts as input(i.e. this receives packages) - Rafael Sampaio
        self.save_protocol_in_simulation_core(self)
    
    def connectionLost(self, reason):
        pass 
      
        
 
class AccessPointFactory(protocol.Factory):

    protocol.ServerFactory.noisy = False
    protocol = AccessPointAppProtocol
    noisy = False
    

    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.listen_protocol = None

    def buildProtocol(self, address):
        proto = protocol.ServerFactory.buildProtocol(self, address)
        self.listen_protocol = proto
        return proto

 
class ClientProtocol(StandardApplicationComponent):
    
    def __init__(self):
        self.simulation_core = None

    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        
    def dataReceived(self, data):
        self.factory.server.write(data)
        
    def connectionLost(self, reason):
        pass     
         
    def write(self, data):
        if data:
            self.transport.write(data)
            

# ============================================== NEW VERSION =============================================================

class AccessPointApp:
        
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.coverage_area_radius = None
        self.TBTT = None
        self._buffer = set()

        # The base device can be a router or switch that use this access point as an input interface - Rafael Sampaio
        self.base_device = None

    def start(self):
        self.draw_connection_to_base_arrow()
        self.passive_scanning()

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

    def draw_connection_to_base_arrow(self):
        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = self.base_device.visual_component.x
        y2 = self.base_device.visual_component.y
        connection_id = self.simulation_core.canvas.create_line(x1,y1,x2,y2, arrow="both", width=1, dash=(4,2))
        self.simulation_core.canvas.after(10, self.update_connection_to_base_arrow, None, connection_id)

    def update_connection_to_base_arrow(self,event, id):
        self.simulation_core.canvas.delete(id)
        self.draw_connection_to_base_arrow()


    def associate(self, device):
        pass

        # def get_nearby_devices_list(self):
        #     all_nearby_device = set()
        # # putting all nearby devices icons in a list that will be use in future to send data across - Rafael Sampaio
        # nearby_devices_icon_list = self.find_nearby_devices_icon()

        # for icon_id in nearby_devices_icon_list:
        #    device = self.WSN_network_group.get_wsn_device_by_icon(icon_id)

        #    if device != None:
        #     all_nearby_device.add(device)

        # return all_nearby_device


    # def get_device_by_icon(self, icon_id):
    #     try:
    #         founded_device = None
            
    #         for device in self.sensors_list:
    #             if device.visual_component.draggable_img == icon_id:
    #                 founded_device = device
            
    #         for device in self.sink_list:
    #             if device.visual_component.draggable_img == icon_id:
    #                 founded_device = device

    #         if founded_device != None:
    #             return founded_device

    #     except Exception as e:
    #         pass
