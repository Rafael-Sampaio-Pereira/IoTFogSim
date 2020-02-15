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
                "topic": "sensor_metering",
                "content": str(random.uniform(10.5,17.5))+"KWH"
            }

        package = self.build_package(msg)
        self.send(package)

        print(package)

        reactor.callLater(self.publish_interval, self.publish)

    
    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data) 
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from broker %s"%(payload))
        self.simulation_core.updateEventsCounter("MQTT response received")


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

        self.publish_interval = 15

        self.network_settings = "tcp:{}:{}".format(self.router_addr,self.router_port)

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.subscribe()        

    def subscribe(self):
        self.simulation_core.updateEventsCounter("sending MQTT REQUEST")
        
        msg = {
                "action": "subscribe",
                "topic": "sensor_metering",
                "content": "None"
            }

        package = self.build_package(msg)
        self.send(package)

        print(package)
        

    
    def dataReceived(self, data):
         
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data)
        
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from broker %s"%(payload))
        self.simulation_core.updateEventsCounter("MQTT response received")

    
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
        self._buffer = []

        sensor_metering = MqttTopic("sensor_metering","A topic for environment sensor monitoring")
        self.topics.append(sensor_metering)

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connection received")
        #self.send(b"test data")
        
    def dataReceived(self, data):        

        self.put_package_in_buffer(data)

        for package in self._buffer:

            destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
            # Print the received data on the sreen.  - Rafael Sampaio
            self.update_alert_message_on_screen(payload)
            #log.msg("Received from client %s"%(payload))

            action, topic_title, content = extract_mqtt_contents(payload)
        
            if action == "publish":

                topic = self.getTopic(topic_title)
                is_register_publisher = self.verify_if_a_publisher_already_in_publishers_list(topic, self)
                response_package = self.build_package("MQTT_ACK")
                self.send(response_package)
                self.simulation_core.updateEventsCounter("Sending MQTT RESPONSE")

                self._buffer.remove(package)

                #SEND TO ALL

            elif action == "subscribe":
                topic = self.getTopic(topic_title)
                is_register_subscriber = self.verify_if_a_subscriber_already_in_subscribers_list(topic, self)
                response_package = self.build_package("MQTT_ACK")
                self.send(response_package)
                self.simulation_core.updateEventsCounter("Sending MQTT RESPONSE")

                self._buffer.remove(package)


            print(self._buffer)



    def getTopic(self, topic_title):

        for topic in self.topics:
            if topic.title == topic_title:
                return topic

    def verify_if_a_publisher_already_in_publishers_list(self, topic, publisher_protocol):
        try:
            # Verify if is some publicher connected - Rafael Sampaio
            if len(topic.publishers)>0:
                for publisher in topic.publishers:
                    # verify if the connected publisher protocol already in the topic publishers list - Rafael Sampaio
                    if self == publisher:
                        return True
                    # if the connected publisher protocol is not in the publishers list, register it in that list - Rafael Sampaio  
                    else:
                        topic.register_publisher(publisher_protocol)
                        log.msg("Publisher registred")
                        return True
            # if there is no connected publisher protocol in the publishers list, register the connected protocol in the list in that list - Rafael Sampaio  
            else:
                topic.register_publisher(publisher_protocol)
                log.msg("Publisher registred")
                return True

        except Exception as e:
            print(e)


    def verify_if_a_subscriber_already_in_subscribers_list(self, topic, subscribe_protocol):
        try:
            # Verify if is some subscriber connected - Rafael Sampaio
            if len(topic.subscribers)>0:
                for subscriber in topic.subscribers:
                    # verify if the connected subscriber protocol already in the topic subscribers list - Rafael Sampaio
                    if self == subscriber:
                        return True
                    # if the connected subscriber protocol is not in the subscribers list, register it in that list - Rafael Sampaio  
                    else:
                        topic.register_subscriber(subscriber_protocol)
                        log.msg("subscriber registred")
                        return True
            # if there is no connected subscriber protocol in the subscribers list, register the connected protocol in the list in that list - Rafael Sampaio  
            else:
                topic.register_subscriber(publisher_protocol)
                log.msg("subscriber registred")
                return True

        except Exception as e:
            print(e)




def extract_mqtt_contents(package):
        
    try:
        package = json.dumps(package)
        #package = package.decode("utf-8")
        package = str(package)[0:]
        print(package)
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

    
    def register_publisher(self, publisher_protocol):
        self.publishers.append(publisher_protocol)

    def register_subscriber(self, subscriber_protocol):
        self.subscribers.append(subscriber_protocol)


MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}