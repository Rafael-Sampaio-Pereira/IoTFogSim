
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp
from twisted.internet import reactor
from random import randint
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
        "task_id": str(uuid.uuid4().fields[-1]),
        "MI": str(TASK_SIZE_CHOICES.get('small'))
    }


class BaseMQTT(object):
    def __init__(self):
        self.broker_addresses = ['192.168.0.2:5800']
        self.has_subscription = False
        self.default_target_topic =  None
    
    def main(self):
        super().main()
        LoopingCall(self.main_loop).start(
            self.simulation_core.clock.get_internal_time_unit(10)
        )
    
    def send_subscribe_request(self):
        for broker_addr in self.broker_addresses:
            broker_ip, broker_port = broker_addr.split(':')
            self.send_packet(
                broker_ip,
                int(broker_port),
                {
                    "action": "subscribe",
                    "topic": self.default_target_topic
                },
                DEFAULT_PACKET_LENGTH
            )

    def check_if_has_subscription(self):
        if not self.has_subscription:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if 'accepted' in packet.payload:
                        self.has_subscription = True
                        self.simulation_core.updateEventsCounter(
                            f"{self.name}-{self.protocol} - Subscribed Successfuly \
                            packet {packet.id}. Payload: {packet.payload}"
                        )
                        self.in_buffer.remove(packet)
                        del packet
    


class PublisherApp(BaseApp, BaseMQTT):

    def __init__(self):
        super(PublisherApp, self).__init__()
        self.port = 5000
        self.name ='MQTT Publisher'
        # self.servers_address = ['192.168.0.2', '192.168.1.2', '172.148.0.2']
        self.default_target_topic = 'task_performers'
        
    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            if self.has_subscription:
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
            else:
                self.check_if_has_subscription()


class SubscriberApp(BaseApp):

    def __init__(self):
        super(SubscriberApp, self).__init__()
        self.port = 3000
        self.name ='MQTT Subscriber'
        # self.servers_address = ['192.168.0.2', '192.168.1.2', '172.148.0.2']
        self.broker_addresses = ['192.168.0.2:5800']
        self.has_subscription = False
        self.default_target_topics = ['task_results', 'resource_availability']
        self.default_listen_topic = 'task_performers'

        
    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            if self.has_subscription:
                for broker_addr in self.broker_addresses:
                    broker_ip, broker_port = broker_addr.split(':')
                    cont+=1
                    interval = self.simulation_core.\
                    clock.get_internal_time_unit(
                        cont*10.0
                    )
                    reactor.callLater(
                        interval, 
                        self.send_packet,
                        broker_ip,
                        int(broker_port),
                        generate_task(),
                        DEFAULT_PACKET_LENGTH
                    )
            else:
                self.check_if_has_subscription()
                
    def perform_next_task_in_buffer(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                if 'task_id' in packet.payload:
                    pass
