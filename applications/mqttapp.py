from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs
import random
import sys
import os

from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

from applications.applicationcomponent import StandardApplicationComponent


class PublisherApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100 

        self.router_addr = "127.0.0.1"
        self.router_port = 8081

        self.publish_interval = 5

        self._buffer = []

        self.network_settings = "tcp:{}:{}".format(self.router_addr,self.router_port)

    def connectionMade(self):
        #self.simulation_core.updateEventsCounter("Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.publish()
        self.update_name_on_screen(self.transport.getHost().host+":"+str(self.transport.getHost().port))          

    def publish(self):
       # self.simulation_core.updateEventsCounter("sending MQTT REQUEST")
        
        msg = {
                "action": "publish",
                "topic": "sensor_metering",
                "content": str(round(random.uniform(2.5,22.5), 2))+" Kwh"
            }

        package = self.build_package(msg)
        self.send(package)
        reactor.callLater(self.publish_interval, self.publish)

    
    def dataReceived(self, data):
       
        self.put_package_in_buffer(data)

        for package in self._buffer:
            destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
            # Print the received data on the sreen.  - Rafael Sampaio
            self.update_alert_message_on_screen(payload)
            #log.msg("PUBLISHER Received from broker %s"%(payload))
            #self.simulation_core.updateEventsCounter("MQTT response received")

class SubscriberApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100 

        self.router_addr = "127.0.0.1"
        self.router_port = 8081

        self._buffer = []

        self.network_settings = "tcp:{}:{}".format(self.router_addr,self.router_port)

    def connectionMade(self):
        #self.simulation_core.updateEventsCounter("Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.subscribe()
        self.update_name_on_screen(self.transport.getHost().host+":"+str(self.transport.getHost().port))       

    def subscribe(self):
        #self.simulation_core.updateEventsCounter("sending MQTT REQUEST")
        
        msg = {
                "action": "subscribe",
                "topic": "sensor_metering",
                "content": "None"
            }

        package = self.build_package(msg)
        self.send(package)


    def dataReceived(self, data):
         
        print("RECEBIDO %s"%(str(data)))

        self.put_package_in_buffer(data)

        for package in self._buffer:
            destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
            # Print the received data on the sreen.  - Rafael Sampaio
            self.update_alert_message_on_screen(payload)
            #log.msg("SUBSCRIBER Received from broker %s"%(payload))
            #self.simulation_core.updateEventsCounter("MQTT response received")


class BrokerApp:

    def start(self, addr, port):
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(BrokerFactory())

class BrokerProtocol(StandardApplicationComponent):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        for c in self.factory.subscribers:
            self.source_addr = c.transport.getHost().host
            self.source_port = c.transport.getHost().port
            self.destiny_addr = c.transport.getPeer().host
            self.destiny_port = c.transport.getPeer().port
            response_package = self.build_package("MQTT_ACK")
            
            c.send(response_package)

    def connectionLost(self, reason):
        self.factory.subscribers.remove(self)

    def dataReceived(self, package):

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
        # Print the received data on the sreen.  - Rafael Sampaio
        #self.update_alert_message_on_screen(payload)

        action, topic_title, content = extract_mqtt_contents(payload)

        if action == "subscribe":
            self.factory.subscribers.add(self)
            self.send_mqtt_acknowledgement(source_addr, source_port)

        elif action == "publish":
            # send ack to the sender of the received package - Rafael Sampaio
            self.send_mqtt_acknowledgement(source_addr, source_port)
            self.send_package_to_all_subscribers(package)

    def send_package_to_all_subscribers(self, package):
        
        for c in self.factory.subscribers:
            self.source_addr = c.transport.getHost().host
            self.source_port = c.transport.getHost().port
            self.destiny_addr = c.transport.getPeer().host
            self.destiny_port = c.transport.getPeer().port

            c.send(package)

    def send_mqtt_acknowledgement(self, destiny_addr, destiny_port):
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        response_package = self.build_package("MQTT_ACK")
        self.send(response_package)

class BrokerFactory(protocol.Factory):
    def __init__(self):
        self.subscribers = set()

    def buildProtocol(self, addr):
        return BrokerProtocol(self)


def extract_mqtt_contents(package):
        
    try:
        package = json.dumps(package)
        #package = package.decode("utf-8")
        package = str(package)[0:]
        json_msg = json.loads(package)

        return json_msg["action"], json_msg["topic"], json_msg["content"]
    
    except Exception as e:
        log.msg(e)

    
MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}


