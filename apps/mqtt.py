from datetime import datetime
import json
from queue import Queue
from twisted.internet.task import LoopingCall
from twisted.python import log
from apps.base_app import BaseApp
from twisted.internet import reactor
from random import randint
import random
import uuid
from operator import attrgetter 



DEFAULT_PACKET_LENGTH = 1024

# Task sizes based on fognetsim++ models
TASK_SIZE_CHOICES = {
    'large': 1500,
    'medium': 900,
    'small': 200,
    'random': randint(200, 1500)
}


class BaseMQTT(BaseApp):

    def __init__(self):
        super(BaseMQTT, self).__init__()
        self.broker_addresses = []
        self.has_subscription = False
        self.target_topics =  None
        self.listen_topics = None
        self.main_interval = 10
        
    def main(self):
        super().main()
        self.send_subscribe_request()
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(self.main_interval)
        )
        
    def check_for_hardware_MIPS(self):
        if self.machine.MIPS:
            self.available_MIPS = self.machine.MIPS
            self.max_MIPS = self.machine.MIPS

    def send_subscribe_request(self):
        if len(self.listen_topics) > 0:
            for broker_addr in self.broker_addresses:
                broker_ip, broker_port = broker_addr.split(':')
                for topic in self.listen_topics:
                    self.send_packet(
                        broker_ip,
                        int(broker_port),
                        {
                            "action": "subscribe",
                            "topic": topic
                        },
                        DEFAULT_PACKET_LENGTH
                    )

    


class PublisherApp(BaseMQTT):

    def __init__(self):
        super(PublisherApp, self).__init__()
        self.port = 5000
        self.name = 'MQTT Publisher'
        # self.servers_address = ['192.168.0.2', '192.168.1.2', '172.148.0.2']
        self.target_topics = ['task_performers']
        self.listen_topics = []
        self.broker_addresses = ['192.168.0.2:5800']
        self.main_interval = 1
        
    def generate_task(self):
        if self.simulation_core.global_seed:
            random.seed(self.simulation_core.global_seed)
        return {
            "topic": self.target_topics[0],
            "action": "publish",
            "task_id": str(uuid.uuid4().fields[-1]),
            "MI": str(TASK_SIZE_CHOICES['medium'])
            # "MI": str(random.choice(list(TASK_SIZE_CHOICES.values())) or 0)
        }

    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            for broker_addr in self.broker_addresses:
                broker_ip, broker_port = broker_addr.split(':')
                cont+=1
                interval = self.simulation_core.\
                clock.get_internal_time_unit(
                    cont*10.0
                )
                # Continuosly send tasks to broker
                reactor.callLater(
                    interval,
                    self.send_packet,
                    broker_ip,
                    int(broker_port),
                    self.generate_task(),
                    DEFAULT_PACKET_LENGTH
                )



class SubscriberApp(BaseMQTT):

    def __init__(self):
        super(SubscriberApp, self).__init__()
        self.port = 3000
        self.name ='MQTT Subscriber'
        # self.servers_address = ['192.168.0.2', '192.168.1.2', '172.148.0.2']
        self.broker_addresses = ['192.168.0.2:5800']
        self.has_subscription = False
        self.target_topics = ['task_results']
        self.listen_topics = ['task_performers']
        self.max_MIPS = None
        self.available_MIPS = None
        
    def main(self):
        super().main()
        self.send_subscribe_request()
        LoopingCall(self.send_resource_availability_to_broker).start(
            self.simulation_core.clock.get_internal_time_unit(0.5)
        )
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(self.main_interval)
        )
        

    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            
            if self.has_subscription:
                self.perform_all_task_in_packet_buffer()
            else:
                self.check_for_hardware_MIPS()
                self.check_if_has_subscription()
                
    def incrase_available_MIPS(self, value):
        self.available_MIPS += value

    def perform_all_task_in_packet_buffer(self):
        """ Performs the task into next packet in the buffer """
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                if 'MI' in packet.payload:
                    packet_task_size = int(packet.payload['MI'])
                    
                    # Verify if there is MIPS capability available
                    # to perform the next task on buffer, if not, it will wait
                    if  self.available_MIPS >= packet_task_size:
                        try:
                            
                            # Subtract task size from available MIPS
                            self.available_MIPS = self.available_MIPS - packet_task_size
                            

                            # set processor busy time for this task perform
                            schedule_interval = self.simulation_core.\
                            clock.get_internal_time_unit(5)

                            # After process time, give back the subtracted
                            # value to the available MIPS by using sum() function
                            reactor.callLater(
                                schedule_interval,
                                self.incrase_available_MIPS,
                                packet_task_size
                            )
                            
                            self.simulation_core.updateEventsCounter(
                                f"{self.name}-{self.protocol} - "+
                                    f"Task {packet.payload['task_id']} "+
                                    f"MI size {packet.payload['MI']} "+
                                    "Performaned"
                            )

                            # After performing task, remove it packet from buffer
                            self.in_buffer.remove(packet)
                            del packet
                            del packet_task_size


                        except Exception as error:
                            log.msg(f"Info :  - | {self.machine.type} "+
                                f"({self.machine.network_interfaces[0].ip}) "+
                                f"Can not perform task due a error: {str(error)}")

    def send_resource_availability_to_broker(self):
        """ Tells the server the current MIPS resource availability """
        if self.max_MIPS and self.available_MIPS:
            for broker_addr in self.broker_addresses:
                broker_ip, broker_port = broker_addr.split(':')
                self.send_packet(
                    broker_ip,
                    int(broker_port),
                    {
                        'action': 'resource',
                        'name': self.machine.name,
                        'max_capacity': self.max_MIPS,
                        'available_capacity': self.available_MIPS
                    },
                    DEFAULT_PACKET_LENGTH
                )
            self.simulation_core.updateEventsCounter(
                f"{self.name}-{self.protocol} - "+
                "Sending resource availability to broker..."
            )
    
    def check_if_has_subscription(self):
        if not self.has_subscription:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if 'accepted' in packet.payload:
                        if packet.payload['accepted'] is True:
                            self.has_subscription = True
                            self.simulation_core.updateEventsCounter(
                                f"{self.name}-{self.protocol} - "+
                                    "Subscribed Successfuly "+
                                    f"packet {packet.id}. Payload: "+
                                    f"{packet.payload}"
                            )
                            self.in_buffer.remove(packet)
                            del packet

class Topic(object):
    def __init__(self, name, broker):
        self.name = name
        self.broker = broker
        self.subscribers_list = []
        self.resource_list = []
        self.message_queue = []
        LoopingCall(self.handle_message_queue).start(0.5)

    def handle_message_queue(self):
        if len(self.message_queue) > 0:
            if len(self.subscribers_list) > 0:
                message = self.message_queue.pop(0)
                
                major_capacity_resource = max(self.resource_list, key=attrgetter("available_capacity"))
                if major_capacity_resource.available_capacity[0] >=  int(message['MI']):
                    self.broker.send_packet(
                        major_capacity_resource.addr,
                        major_capacity_resource.port,
                        message,
                        DEFAULT_PACKET_LENGTH
                    )
                else:
                    # if major available capacity resource can not perform task
                    # Send it to the Cloud Task Perform Service
                    self.broker.send_packet(
                        self.broker.cloud_addr,
                        self.broker.cloud_port,
                        message,
                        DEFAULT_PACKET_LENGTH,
                        network_interface_indice=1
                    )


class Resource(object):
    def __init__(
        self, name, addr, port, max_capacity, available_capacity, last_update
    ):
        self.name = name
        self.addr = addr
        self.port = port
        self.max_capacity = max_capacity # MIPS
        self.available_capacity = available_capacity # MIPS
        self.last_update = last_update or None

class LoadBalanceBrokerApp(BaseApp):
    def __init__(self):
        super(LoadBalanceBrokerApp, self).__init__()
        self.port = 5800
        self.name ='Load Balance Broker'
        self.main_interval = 1
        self.cloud_addr = '192.168.1.2'
        self.cloud_port = 3000
        self.topics = [
            Topic('task_results', self),
            Topic('task_performers', self),
        ]
        self.topics_names = [topic.name for topic in self.topics]
        self.resources_list = []
        
    def put_resurce_in_topics_based_on_subscriber_ip_and_port(self, ip, port, resource):
        for topic in self.topics:
            if str(ip)+":"+str(port) in topic.subscribers_list:
                topic.resource_list.append(resource)

    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if packet.destiny_port == self.port:
                        self.simulation_core.updateEventsCounter(
                            f"{self.name}-{self.protocol} - "+
                            f"proccessing packet {packet.id}. "+
                            f"Payload: {packet.payload}"
                        )
                        if 'subscribe' in packet.payload['action']:
                            if packet.payload['topic'] in self.topics_names:
                                for topic in self.topics:
                                    
                                    if topic.name == packet.payload['topic']:
                                        topic.subscribers_list.append(
                                            f"{packet.source_addr}:"+
                                            f"{packet.source_port}"
                                        )
                                        self.send_packet(
                                            packet.source_addr,
                                            packet.source_port,
                                            {
                                                "topic": topic.name,
                                                "action": "response",
                                                "accepted": True
                                            },
                                            DEFAULT_PACKET_LENGTH,
                                            packet.last_link,
                                            'red'
                                        )
                            else:
                                self.send_http_response(
                                    404,
                                    'Not Found',
                                    packet.source_addr,
                                    packet.source_port,
                                    DEFAULT_PACKET_LENGTH,
                                    packet.last_link
                                )
                        elif 'publish' in packet.payload['action']:
                            if packet.payload['topic'] in self.topics_names:
                                for topic in self.topics:
                                    if topic.name == packet.payload['topic']:
                                        # Send packet to topic message queue
                                        topic.message_queue.append(
                                            packet.payload
                                        )
                                        self.send_ack(
                                            packet.source_addr,
                                            packet.source_port,
                                            packet.last_link
                                        )
                            else:
                                self.send_http_response(
                                    404,
                                    'Not Found',
                                    packet.source_addr,
                                    packet.source_port,
                                    DEFAULT_PACKET_LENGTH,
                                    packet.last_link
                                )
                        elif 'resource' in packet.payload['action']:
                            resource = self.get_resource_by_machine_ip(
                                packet.source_addr
                            )
                            if resource:
                                # If the resource already mapped, just update
                                resource.available_capacity = packet.payload['available_capacity'],
                                resource.last_update = datetime.now()
                            else:
                                # If there is no a resource that represents the
                                # incoming packet machine, create a new one
                                res = Resource(
                                    name = packet.payload['name'],
                                    addr = packet.source_addr,
                                    port = packet.source_port,
                                    max_capacity = packet.payload['max_capacity'],
                                    available_capacity = packet.payload['available_capacity'],
                                    last_update = datetime.now()
                                )
                                self.resources_list.append(res)
                                self.put_resurce_in_topics_based_on_subscriber_ip_and_port(
                                    packet.source_addr, packet.source_port, res
                                )
                        else:
                            self.send_http_response(
                                403,
                                'Bad Request',
                                packet.source_addr,
                                packet.source_port,
                                DEFAULT_PACKET_LENGTH,
                                packet.last_link
                            )
                        
                    else:
                        self.send_http_response(
                            404,
                            'Not Found',
                            packet.source_addr,
                            packet.source_port,
                            DEFAULT_PACKET_LENGTH,
                            packet.last_link
                        )
                    # After proccessing request it packet from buffer
                    self.in_buffer.remove(packet)
                    del packet
                    
    def get_resource_by_machine_ip(self, ip):
        # filter list by machine ip, if not found, return None
        return next(filter(
                lambda resource: resource.addr == ip,
                self.resources_list), None)

    def main(self):
        super().main()
        self.simulation_core.updateEventsCounter(
            f"{self.name}-{self.protocol} - Start listen on port {self.port}"
        )
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(0.07)
        )

    def send_http_response(
        self, status_code, message, destiny_addr, destiny_port, length, last_link=None):
        self.send_packet(
            destiny_addr,
            destiny_port,
            f'HTTP 1.0 {status_code} - {message}',
            length,
            last_link
        )
    
    def send_ack(self, destiny_addr, destiny_port, last_link):
        self.send_packet(
            destiny_addr,
            destiny_port,
            {
                "action": "response",
                "ack": str(uuid.uuid4().fields[-1])
            },
            DEFAULT_PACKET_LENGTH,
            last_link,
            'red'
        )
        
        
class CloudTaskPerformServerApp(BaseMQTT):

    def __init__(self):
        super(CloudTaskPerformServerApp, self).__init__()
        self.port = 3000
        self.name ='Cloud Task Perform Service'
        self.main_interval = 1
        
    def main(self):
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(self.main_interval)
        )
        
    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            self.perform_next_task_in_packet_buffer()

    def perform_next_task_in_packet_buffer(self):
        """ Performs the task into next packet in the buffer """
        if len(self.in_buffer) > 0:
            next_packet = self.in_buffer[(0 + 1) % len(self.in_buffer)]

            if 'MI' in next_packet.payload:
                next_task_size = int(next_packet.payload['MI'])                
                try:
                    # Removing task from buffer
                    packet = self.in_buffer.pop(0)
                    self.simulation_core.updateEventsCounter(
                        f"{self.name}-{self.protocol} - "+
                            f"Task {next_packet.payload['task_id']} "+
                            f"MI size {next_packet.payload['MI']} "+
                            "Performaned"
                    )

                    # After performing task, remove it packet from buffer
                    del packet
                    del next_task_size
                    del next_packet

                except Exception as error:
                    log.msg(f"Info :  - | {self.machine.type} "+
                        f"({self.machine.network_interfaces[0].ip}) "+
                        f"Can not perform task due a error: {str(error)}")
