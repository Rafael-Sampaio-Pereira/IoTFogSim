
from twisted.internet import protocol, reactor
from twisted.python import log
import json
import uuid
import sys
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

from applications.applicationcomponent import StandardApplicationComponent

from scinetsim.functions import create_csv_database_file

class FogDataReducitonBrokerApp:

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
            self.update_bytes_on_screen(package)

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


    def update_bytes_on_screen(self, package):
        
        try:
            self.factory.total_received_bytes = self.factory.total_received_bytes+int(sys.getsizeof(package))
            msg = "Received Total - "+str(self.factory.total_received_bytes)+" Bytes"+" / "+" Just Received - "+str(sys.getsizeof(package))+" Bytes"
            self.update_alert_message_on_screen(msg)

        except Exception as e:
            log.msg(e)
        


    

class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers = set()
        self.total_received_bytes = 0

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


