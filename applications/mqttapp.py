from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs
import random
import sys
import os
import time
import uuid

from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

from applications.applicationcomponent import StandardApplicationComponent
from scinetsim.dataproducers import energy_consumption_meter



class PublisherApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.screen_name = None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100 

        self.gateway_addr = "127.0.0.1"
        self.gateway_port = 8082

        self.publish_interval = 5

        self._buffer = []

        self.network_settings = "tcp:{}:{}".format(self.gateway_addr,self.gateway_port)

    def connectionMade(self):
        
        # Getting ip and port of the subscriber protocol to compose its name - Rafael Sampaio
        self.screen_name = self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the first publish message with topic and value. it's not a simple connect mesage, it's fisrt data to a topic - Rafael Sampaio
        self.publish()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 
        
        self.create_connection_animation()  

    def publish(self):
                
        msg = {
                "action": "publish",
                "topic": "sensor_metering",
                "content": energy_consumption_meter()
            }

        self.simulation_core.updateEventsCounter(self.screen_name+" - sending MQTT PUBLISH REQUEST")
        package = self.build_package(msg)
        self.send(package)

        # This publish function will be called periodically to the broker - Rafael Sampaio
        reactor.callLater(self.publish_interval, self.publish)

    def dataReceived(self, data):
       
        self.put_package_in_buffer(data)

        try:
            for package in self._buffer:
                destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
                # Print the received data on the sreen.  - Rafael Sampaio
                self.update_alert_message_on_screen(payload)
                #self.simulation_core.updateEventsCounter("MQTT response received")
                #if data in self._buffer:
            
                self._buffer.remove(data)
        except:
            pass

class SubscriberApp(StandardApplicationComponent):
    
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

        self.screen_name = self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the subscribe request - Rafael Sampaio
        self.subscribe()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 

        self.create_connection_animation()    

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
        try:
            for package in self._buffer:
                destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
                # Print the received data on the sreen.  - Rafael Sampaio
                self.update_alert_message_on_screen(payload)
                #self.simulation_core.updateEventsCounter("MQTT response received")
                #if data in self._buffer:
            
            self._buffer.clear()
        except:
            pass
        


class BrokerApp:

    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        
        broker_factory = BrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(addr+":"+str(port))) 

class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.factory = factory
        
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
        response_package = self.build_package("MQTT_ACK")
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
        response_package = self.build_package("MQTT_ACK"+str(uuid.uuid4().fields[-1]))
        self.send(response_package)

class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers = set()

    def buildProtocol(self, addr):
        return BrokerProtocol(self)


def extract_mqtt_contents(package):
    try:
        package = json.dumps(package)
        package = str(package)[0:]
        json_msg = json.loads(package)
        return json_msg["action"], json_msg["topic"], json_msg["content"]
    except Exception as e:
        log.msg(e)

MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}


