
from scinetsim.dataproducers import *
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.python import log
import time
import uuid
import json
import tkinter as tk
from applications.applicationcomponent import StandardApplicationComponent
from scinetsim.functions import create_csv_database_file

from applications.mqttapp import extract_mqtt_contents


class WSNApp(StandardApplicationComponent):
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None

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
            self.visual_component.signal_radius = 10
        
        reactor.callLater(0.1, self.propagate_signal)

    def show_signal(self):
        self.visual_component.signal_radius = self.visual_component.coverage_area_radius
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
        self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle,
                                            self.visual_component.x+self.visual_component.signal_radius, 
                                            self.visual_component.y+self.visual_component.signal_radius, 
                                            self.visual_component.x-self.visual_component.signal_radius, 
                                            self.visual_component.y-self.visual_component.signal_radius)

    
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
            buffer_string += '|'+str(package.data)
        print(self_name, buffer_string)
        print('\n')

    def draw_connection_arrow(self, destiny):
        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = destiny.visual_component.x
        y2 = destiny.visual_component.y
        connection_id = self.simulation_core.canvas.create_line(x1,y1,x2,y2, arrow=tk.LAST, width=3, dash=(4,2))

        self.simulation_core.canvas.after(2, self.delete_connection_arrow, connection_id)

    def delete_connection_arrow(self, id):
        self.simulation_core.canvas.delete(id)

class SensorApp(WSNApp):
    def __init__(self):
        self._buffer = set()
        self.interval = 3
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None
        
    
    def start(self, nearby_devices_list):
        self.name = self.simulation_core.canvas.itemcget(self.visual_component.draggable_name, 'text')
        self.nearby_devices_list = nearby_devices_list
        # self.propagate_signal()
        self.show_signal()
        self.print_node_connections(nearby_devices_list)

        self.collect_and_send_data()


    def collect_and_send_data(self):
        
        # collecting data - Rafael Sampaio
        data = energy_consumption_meter()


        
        # Creating a new package - Rafael Sampaio
        pack = WSNPackage(source = self, data = data)

        # putting this device in the generated package trace - Rafael Sampaio
        pack.put_in_trace(self)

        # putting data in device buffer - Rafael Sampaio
        self._buffer.add(pack) 


        def remove_sent_packages_from_buffer(_package):
            # after send, remove data from buffer - Rafael Sampaio    
            self._buffer.remove(_package)

        if len(self._buffer) > 0:
            self.temp_buffer = self._buffer.copy()
            
            # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
            for _package in self.temp_buffer:
                self.forward_package(_package)
                
                remove_sent_packages_from_buffer(_package)
    
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



class SinkApp(WSNApp):
    def __init__(self):
        self._buffer = set() # this buffer stores only data from the wsn sensors - Rafael Sampaio
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None
        self.sink_factory = None
        self.gateway_addr = '127.0.0.1'
        self.gateway_port = 8081
         # Destiny info (e.g. mqtt broker server addr and port) - Rafael Sampaio
        self.destiny_addr = '127.0.0.1'
        self.destiny_port = 5100
        self.source_addr = None
        self.source_port = None

    def start(self, nearby_devices_list):
        #self.propagate_signal()
        self.show_signal()
        self.connect_to_gateway()
        self.configure_source_info()
        self.forward_packages()

    # this method allow the sink to connect to router/switch - Rafael Sampaio
    def connect_to_gateway(self):
        # get start to connect to gateway - Rafael Sampaio
        factory = SinkAppFactory(self.simulation_core, self.visual_component)
        factory.noisy = False
        reactor.connectTCP(self.gateway_addr, self.gateway_port, factory)
        self.sink_factory = factory


    def configure_source_info(self):
        # get the network info from the sink protocol and using it to set the sink app network info - Rafael Sampaio 
        if self.sink_factory:
            if self.sink_factory.running_protocol:
                if not self.source_addr:
                    self.source_addr = self.sink_factory.running_protocol.source_addr
                
                if not self.source_port:
                    self.source_port = self.sink_factory.running_protocol.source_port

        # while the source info is not complete this function will be recursivelly called - Rafael Sampaio
        if self.source_addr == None or self.source_port == None:
            reactor.callLater(1, self.configure_source_info)



    def forward_packages(self):
        if self.verify_buffer():
            if self.sink_factory.running_protocol and (self.source_addr != None and self.source_port != None):
                
                data = "["
                
                # forwarding packages to the gateway - Rafael Sampaio
                for wsn_package in self._buffer.copy():


                    data += '{ "source": "' + wsn_package.source.name + '", "data": "' + wsn_package.data + '" },'
                    self._buffer.remove(wsn_package)


                data = data[:-1]
                data += "]"

                data = json.loads(data)

                # this method is work into a mqtt context. to execute another scenario, pelase, change this method - Rafael Sampaio
                mqtt_msg = {
                        "action": "publish",
                        "topic": "sensor_metering",
                        "content": data
                    }

                mqtt_package = self.build_package(mqtt_msg)

                # this uses the send method defined in the StandardApplicationComponent class - Rafael Sampaio
                self.sink_factory.running_protocol.send(mqtt_package)
                
        
        reactor.callLater(1, self.forward_packages)

    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False   



class SinkAppFactory(ClientFactory):
    
    def __init__(self, simulation_core, visual_component):
        self.running_protocol = None
        self.visual_component = visual_component
        self.simulation_core =  simulation_core

    def buildProtocol(self, address):
        self.running_protocol = SinkAppProtocol(self.simulation_core, self.visual_component)
        self.running_protocol.save_protocol_in_simulation_core(self.running_protocol) 
        return self.running_protocol


# this protocol acts as a client to the router/switch - Rafael Sampaio
class SinkAppProtocol(StandardApplicationComponent):
    
    def __init__(self, simulation_core, visual_component):
        self.visual_component = visual_component
        self.simulation_core =  simulation_core
        self._buffer = set() # this sink uses only one buffer, you need to pay atention when your application has top-down approachs - Rafael Sampaio
        # the sink network info will be generated after the connection to a gateway such as router or switch - Rafael Sampaio
        self.source_addr = None
        self.source_port = None

    def connectionMade(self):
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.transport.setTcpKeepAlive(1)
        self.terminateLater = None
        self.create_connection_animation()

    # This method is overhidding the dataReceived method in the StandardApplicationComponent class - Rafael Sampaio
    def dataReceived(self, data):
        # this sink uses the bottom-up approach and dont let us to use top-down messages/commands - Rafael Sampaio
        pass

    def connectionLost(self, reason):
        pass     
         
    def write(self, data):
        if data:
            self.transport.write(data)



class WSNPackage(object):
    
    def __init__(self, source,  data):
        self.id = uuid.uuid4().fields[-1]
        self.source = source
        # self.destiny = destiny
        self.data = data
        #self.was_forwarded = False
        self.trace = set()



    def get_package_as_json(self):
        
        all_destiny_names = ''

        package = {
            "id": str(self.id),
            "source": self.source.name,
            "data": self.data
        }

        package = json.dumps(package)

        return package

    
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



class SCADAApp(StandardApplicationComponent):
    # This SCADA App is based on the simple mqtt subscriber App - Rafael Sampaio
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.screen_name = None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100 

        self.gateway_addr = "127.0.0.1"
        self.gateway_port = 8081

        

        self._buffer = []

        self.network_settings = "tcp:{}:{}".format(self.gateway_addr,self.gateway_port)

    def connectionMade(self):
        # creating and opening a csv database file - Rafael Sampaio
        self.database = create_csv_database_file(self.simulation_core)

        self.screen_name = self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the subscribe request - Rafael Sampaio
        self.subscribe()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 

        self.create_connection_animation()

        self.save_to_database()   

    def subscribe(self):
                
        msg = {
                "action": "subscribe",
                "topic": "sensor_metering",
                "content": "None"
            }

        self.simulation_core.updateEventsCounter(self.screen_name+" - sending MQTT SUBSCRIBE REQUEST")
        package = self.build_package(msg)
        self.send(package)

    def dataReceived(self, data):
        self.put_package_in_buffer(data)


    def extract_energy_content(self, payload):
        pass

    def save_to_database(self):

        try:
            if self.verify_buffer():
                
                for package in self._buffer.copy():
                    destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
                                        
                    payload = json.dumps(payload)
                    
                    if payload.startswith('{'):

                        payload = json.loads(payload)

                        to_file = ""

                        # extract energy content - Rafael Sampaio
                        for obj in payload['content']:
                            to_file = obj['source']+","+ obj['data']
                            
                            print(to_file, file = self.database, flush=True)

                        # Print the received data on the sreen.  - Rafael Sampaio
                        self.update_alert_message_on_screen(payload['content'])

                        self._buffer.remove(package)
                    
                    else:
                        # Print the received data on the sreen.  - Rafael Sampaio
                        self.update_alert_message_on_screen(payload)

                        self._buffer.remove(package)


        except Exception as e:
            log.msg(e)
        
        reactor.callLater(1, self.save_to_database)


    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False 




class RepeaterApp(WSNApp):
    def __init__(self):
        self._buffer = set()
        self.interval = 3
        self.simulation_core = None
        self.visual_component = None
        self.nearby_devices_list = None
        
    
    def start(self, nearby_devices_list):
        self.name = self.simulation_core.canvas.itemcget(self.visual_component.draggable_name, 'text')
        self.nearby_devices_list = nearby_devices_list
        #self.propagate_signal()
        self.show_signal()
        self.print_node_connections(nearby_devices_list)

        self.route_packages()


    def route_packages(self):
        
        def remove_sent_packages_from_buffer(_package):
            # after send, remove data from buffer - Rafael Sampaio    
            self._buffer.remove(_package)

        if len(self._buffer) > 0:
            self.temp_buffer = self._buffer.copy()
            
            # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
            for _package in self.temp_buffer:
                self.forward_package(_package)
                            
                remove_sent_packages_from_buffer(_package)
    
        reactor.callLater(self.interval, self.route_packages)

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

                        self.simulation_core.updateEventsCounter("wsn repeater node routing data")