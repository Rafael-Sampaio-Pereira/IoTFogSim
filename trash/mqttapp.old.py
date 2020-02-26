from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs
import random 

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
        self.destiny_port = 5000 

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

    

    
class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = self.factory.visual_component
        self.simulation_core = self.factory.simulation_core

        self.source_addr = "127.0.0.1"
        self.source_port = 5000 

        self.destiny_addr = None
        self.destiny_port = None

        self.router_addr = "127.0.0.1"
        self.router_port = 8081

        self.network_settings = "tcp:interface={}:{}".format(str(self.router_addr),self.router_port)

        self.topics = []
        self._buffer = []
        self.factory = None

        sensor_metering = MqttTopic("sensor_metering","A topic for environment sensor monitoring")
        self.topics.append(sensor_metering)

        

    def connectionMade(self):
        self.update_name_on_screen(self.transport.getHost().host+":"+str(self.transport.getHost().port)) 
        
        #self.simulation_core.updateEventsCounter("Connection received")
        #self.send(b"test data")
        
    def dataReceived(self, data): 
        
        #print(self.transport.getPeer)       

        self.put_package_in_buffer(data)

        for package in self._buffer:

            #print(package)

            destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
            # Print the received data on the sreen.  - Rafael Sampaio
            self.update_alert_message_on_screen(payload)
            #log.msg("Received from client %s"%(payload))

            action, topic_title, content = extract_mqtt_contents(payload)

            topic = self.getTopic(topic_title)
        
            if action == "publish":
                print("AQUIIIIIIIIIIIIIIIII")
                
                
                self.destiny_addr = source_addr
                self.destiny_port = source_port
                

                response_package = self.build_package("MQTT_ACK")


                #print("RESPONDENDO->> %s"%(str(response_package)))

                self.send(response_package)
                #self.simulation_core.updateEventsCounter("Sending MQTT RESPONSE")



                #falta salvar o SUBSCRIBER NA LISTA E ENVIAR MENSAGENS PRA ELE

                print(len(topic.subscribers))
                subscribers_list = list(map(str, topic.subscribers))
                print(subscribers_list)
                for subscriber in subscribers_list:
  
                    destiny_info = subscriber.split(':')

                    print(destiny_info)
                    



            elif action == "subscribe":

                subscriber = source_addr+":"+str(source_port)
                topic.subscribers.append(subscriber)

                print(len(topic.subscribers))
                print(topic.subscribers)

                self.destiny_addr = source_addr
                self.destiny_port = source_port
                
                
                response_package = self.build_package("MQTT_ACK"+str(round(random.uniform(2.5,22.5), 2)))

                self.send(response_package)
                #self.simulation_core.updateEventsCounter("Sending MQTT RESPONSE")

                self._buffer.remove(package)



    def getTopic(self, topic_title):

        for topic in self.topics:
            if topic.title == topic_title:
                return topic

  



class BrokerApp:
    
    def __init__(self):
        self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None

    def start(self, addr, port):
        try:
            factory = BrokerFactory()
            factory.protocol.noisy = False
            #factory.protocol = BrokerProtocol
            factory.protocol.factory = factory
            factory.simulation_core = self.simulation_core
            factory.visual_component = self.visual_component
            factory.all_connectors_list = self.all_connectors_list
            reactor.listenTCP(port, factory, interface=addr)

        except Exception as e:
            log.msg("Error: %s" % str(e))



def extract_mqtt_contents(package):
        
    try:
        package = json.dumps(package)
        #package = package.decode("utf-8")
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

    
    def register_publisher(self, publisher):
        self.publishers.append(publisher)

    def register_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
    
    def send_to_all_subscribers(self, package):
        for subscriber in self.subscribers:
            subscriber.send(package)







class BrokerFactory(protocol.ServerFactory):
    protocol = BrokerProtocol

    def __init__(self):
        self.clients = []


MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}


