from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs

from applications.applicationcomponent import StandardApplicationComponent


class PublisherApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5000 

        self.router_addr = "127.0.0.1"
        self.router_port = 8081

        self.publish_interval = 10


        self.network_settings = "tcp:{}:{}".format(self.router_addr,self.router_port)

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.publish()        

    def publish(self):
        self.simulation_core.updateEventsCounter("sending MQTT REQUEST")
        
        msg = {
                "action": "publish",
                "topic": "sensors",
                "content": "25w"
            }

        package = self.build_package(msg)
        self.send(package)
        reactor.callLater(self.publish_interval, self.publish)

    
    

    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data) 
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from broker %s"%(payload))
        self.simulation_core.updateEventsCounter("Http response received")

    
class BrokerApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core = None

        self.source_addr = "127.0.0.1"
        self.source_port = 5000 

        self.destiny_addr = None
        self.destiny_port = None

        self.router_addr = "127.0.0.1"
        self.router_port = 80

        self.network_settings = "tcp:interface={}:{}".format(str(self.router_addr),self.router_port)

        self.topics = []

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connection received")
        #self.send(b"test data")
        
    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data)
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from client %s"%(payload))

        msg = {
                "action": "response",
                "topic": "sensors",
                "content": "MQTT_ACK"
            }

        package = self.build_package(msg)
        self.send(package)

        self.simulation_core.updateEventsCounter("Sending MQTT RESPONSE")



def extract_mqtt_contents(self, package):
        
    try:
        package = package.decode("utf-8")
        package = str(package)[0:]
        json_msg = json.loads(package)

        return json_msg["action"], json_msg["topic"], json_msg["content"]
    
    except Exception as e:
        log.msg(e)
        
    

class MqttTopic(object):
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.publishers = []
        self.subscribers = []
