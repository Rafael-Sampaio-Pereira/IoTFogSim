import json
from twisted.internet.task import LoopingCall
from twisted.python import log
from apps.base_app import BaseApp
from twisted.internet import reactor
from random import randint
import random
import uuid


DEFAULT_PACKET_LENGTH = 1024

TASK_SIZE_CHOICES = {
    'large': 1500,
    'medium': 900,
    'small': 200,
    'random': randint(200, 1500)
}

def generate_task():
    return {
        "action": "publish",
        "task_id": str(uuid.uuid4().fields[-1]),
        "MI": str(TASK_SIZE_CHOICES.get('small') or 0)
    }


class BaseMQTT(BaseApp):

    def __init__(self):
        super(BaseMQTT, self).__init__()
        self.broker_addresses = []
        self.has_subscription = False
        self.target_topics =  None
        
    def main(self):
        super().main()
        self.send_subscribe_request()
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(10)
        )
        
    def check_for_hardware_MIPS(self):
        if self.machine.MIPS:
            self.available_MPIS = self.machine.MIPS

    def send_subscribe_request(self):
        for broker_addr in self.broker_addresses:
            broker_ip, broker_port = broker_addr.split(':')
            self.send_packet(
                broker_ip,
                int(broker_port),
                {
                    "action": "subscribe",
                    "topic": self.target_topics[0]
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
        self.broker_addresses = ['192.168.0.2:5800']

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
                    generate_task(),
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
        self.target_topics = ['task_results', 'resource_availability']
        self.listen_topics = ['task_performers']

    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            if self.has_subscription:
                self.perform_next_task_in_packet_buffer()
            else:
                self.check_for_hardware_MIPS()
                self.check_if_has_subscription()

    def perform_next_task_in_packet_buffer(self):
        """ Performs the task into next packet in the buffer """
        if len(self.in_buffer) > 0:
            next_packet = self.in_buffer[(0 + 1) % len(self.in_buffer)]

            if 'MI' in next_packet.payload:
                next_task_size = int(next_packet.payload['MI'])

                # Verify if there is MIPS capability available
                # to perform the next task on buffer, if not, it will wait
                if  self.available_MPIS > next_task_size:

                    try:
                        # Subtract task size from available MPIS
                        self.available_MPIS -= next_task_size

                        # Removing task from buffer
                        packet = self.in_buffer.pop(0)

                        # set processor busy time for this task perform
                        schedule_interval = self.simulation_core.\
                        clock.get_internal_time_unit(1)

                        # After process time, give back the subtracted
                        # value to the available MPIS by using sum() function
                        reactor.callLater(
                            schedule_interval,
                            sum,
                            self.available_MPIS,
                            next_task_size
                        )

                        # After performing task, remove it packet from buffer
                        self.in_buffer.remove(packet)
                        del packet
                        del next_task_size
                        del next_packet

                    except Exception as error:
                        log.msg(f"Info :  - | {self.machine.type} "+
                            f"({self.machine.network_interfaces[0].ip}) "+
                            f"Can not perform task due a error: {str(error)}")
                        

    def send_resource_availability_to_broker(self):
        """ Tells the server the current MIPS resource availability """
        for broker_addr in self.broker_addresses:
            broker_ip, broker_port = broker_addr.split(':')
            self.send_packet(
                broker_ip,
                int(broker_port),
                {
                    "action": "publish",
                    "topic": self.target_topics[1]
                },
                DEFAULT_PACKET_LENGTH
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
        self.subscriber_list = []

class LoadBalanceBrokerApp(BaseApp):
    def __init__(self):
        super(LoadBalanceBrokerApp, self).__init__()
        self.port = 5800
        self.name ='Load Balance Broker'
        self.topics = [
            Topic('task_results', self),
            Topic('task_performers', self),
            Topic('resource_availability', self)
        ]
        self.topics_names = [topic.name for topic in self.topics]

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
                                        topic.subscriber_list.append(
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
                                            DEFAULT_PACKET_LENGTH
                                        )
                            else:
                                self.send_http_response(
                                    404,
                                    'Not Found',
                                    packet.source_addr,
                                    packet.source_port,
                                    DEFAULT_PACKET_LENGTH
                                )
                        elif 'publish' in packet.payload['action']:
                            pass
                        else:
                            self.send_http_response(
                                403,
                                'Bad Request',
                                packet.source_addr,
                                packet.source_port,
                                DEFAULT_PACKET_LENGTH
                            )
                        
                    else:
                        self.send_http_response(
                            404,
                            'Not Found',
                            packet.source_addr,
                            packet.source_port,
                            DEFAULT_PACKET_LENGTH
                        )
                    # After proccessing request it packet from buffer
                    self.in_buffer.remove(packet)
                    del packet
                        
    def main(self):
        super().main()
        self.simulation_core.updateEventsCounter(
            f"{self.name}-{self.protocol} - Start listen on port {self.port}"
        )
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(0.07)
        )

    def send_http_response(
        self, status_code, message, destiny_addr, destiny_port, length):
        self.send_packet(
            destiny_addr,
            destiny_port,
            f'HTTP 1.0 {status_code} - {message}',
            length
        )
        
        
# cloud não tem está com o has_subscription == true mesmo depois de enviar a request