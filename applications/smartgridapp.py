
from twisted.internet import protocol, reactor
from twisted.python import log
import json
import uuid
import sys
from datetime import datetime
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet.task import LoopingCall
from applications.applicationcomponent import StandardApplicationComponent

from core.functions import create_csv_database_file, extract_mqtt_contents

class FogBrokerApp:

    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        
        broker_factory = BrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text="\n\n\nAGREGADOR\n"+str(addr+":"+str(port))) 

class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.factory = factory
        self.database = False
        

    def connectionLost(self, reason):        
        try:
            if self in factory.subscribers:
                self.factory.subscribers.remove(self)
        except NameError:
            pass
    
    def connectionMade(self):
        self.visual_component = self.factory.visual_component
        self.simulation_core =  self.factory.simulation_core
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.destiny_addr = self.transport.getPeer().host
        self.destiny_port = self.transport.getPeer().port
        response_package = self.build_package("MQTT_ACK", 'mqtt')
        self.send(response_package)
        self.save_protocol_in_simulation_core(self)
        
        

    def dataReceived(self, package):

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
        # Print the received data on the sreen.  - Rafael Sampaio

        action, topic_title, content = extract_mqtt_contents(payload)

        if action == "subscribe":
            # Saving the connected protocol to the factory subscribers protocols list set - Rafael Sampaio
            self.factory.subscribers.add(self)
            self.send_mqtt_acknowledgement(source_addr, source_port)

        elif action == "publish":
            # send ack to the sender of the received package - Rafael Sampaio
            self.send_mqtt_acknowledgement(source_addr, source_port)
            self.send_package_to_all_subscribers(package)
            self.update_last_package_received_time_on_screen(package)

    def send_package_to_all_subscribers(self, package):
        
        for subscriber in self.factory.subscribers:
            self.source_addr = subscriber.transport.getHost().host
            self.source_port = subscriber.transport.getHost().port
            self.destiny_addr = subscriber.transport.getPeer().host
            self.destiny_port = subscriber.transport.getPeer().port
            subscriber.send(package)

    def send_mqtt_acknowledgement(self, destiny_addr, destiny_port):
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        response_package = self.build_package("MQTT_ACK"+str(uuid.uuid4().fields[-1]), 'mqtt')
        self.send(response_package)


    def update_last_package_received_time_on_screen(self, package):
        format = "%d/%m/%Y - %H:%M:%S"
        now = datetime.now()
        now = now.strftime(format)

        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now+"\n")

        


    

class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers = set()
        self.total_received_bytes = 0

    def buildProtocol(self, addr):
        return BrokerProtocol(self)

MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}





# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||



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

        self.screen_name = "\n\n      SCADA\n"+self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the subscribe request - Rafael Sampaio
        self.subscribe()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 

        self.create_connection_animation()

        # self.save_to_database()
        LoopingCall(self.save_to_database).start(32.0)  

    def subscribe(self):
                
        msg = {
                "action": "subscribe",
                "topic": "sensor_metering",
                "content": "None"
            }

        self.simulation_core.updateEventsCounter(self.screen_name+" - sending MQTT SUBSCRIBE REQUEST")
        package = self.build_package(msg, 'mqtt')
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
                            data = json.loads(json.dumps(obj['data']))
                            to_file = obj['id']+","+obj['source']+","+data['voltage']+","+data['current']+","+data['frequency']+","+data['active_power']+","+data['aparent_power']+","+data['power_factor']+","+ obj['created_at']+","+"stored_at:"+datetime.now().isoformat()
                            
                            print(to_file, file = self.database, flush=True)

                            

                        # Print the received data on the sreen.  - Rafael Sampaio
                        # self.update_alert_message_on_screen(payload['content'])

                        format = "%d/%m/%Y - %H:%M:%S"
                        now = datetime.now()
                        now = now.strftime(format)

                        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
                        self.update_alert_message_on_screen("Last received:"+now)

                        self._buffer.remove(package)
                    
                    else:
                        # Print the received data on the sreen.  - Rafael Sampaio
                        self.update_alert_message_on_screen(payload)

                        self._buffer.remove(package)
                
                self.simulation_core.updateEventsCounter("SCADA - Saving to the database.")


        except Exception as e:
            log.msg(e)
        
        # reactor.callLater(1, self.save_to_database)


    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False 

