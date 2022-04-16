from datetime import datetime
from collections import defaultdict
import json
from collections import deque
from random import random, randint
from sched import scheduler
from applications.mobilityapp import MobileProducerApp
from twisted.internet import protocol, reactor
from twisted.python import log
import uuid
import socket

from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import reactor, protocol, endpoints
from twisted.internet.task import LoopingCall
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import connectProtocol
from applications.applicationcomponent import StandardApplicationComponent
from core.functions import extract_mqtt_contents

from twisted.internet.protocol import Factory

# This removes start/stop factory logs - Rafael Sampaio
Factory.noisy = False

TASKS = {
    'large': 1500,
    'medium': 900,
    'small': 200,
    'random': randint(200, 1500)
}
DEFAULT_FOG_NODE_MIPS_CAPACITY = 3000


class TaskGeneratorApp(MobileProducerApp):
    """
#     This is based on in the MQTT MobileProducerApp.
#     This Acts as a Publisher component send tasks to the 'task' mqtt topic.
#     This generates MIPS task and send to OchesrtrationBrokerApp, so broker can
#     send tasks to computeApps(Subscribers)
#     """

    def generate_data(self):
        data = '{"task": "'+str(TASKS.get('small'))+'"}'
        return data

class ComputeApp(StandardApplicationComponent):
    """
    This is based on in the MQTT SubscriberApp.
    This Acts as a Subscriber component listen to 'task' mqtt topic.
    This Acts as a Publisher component send task result mqtt topic.
    This receives MIPS task from OchesrtrationBrokerApp and performs that
    """

    def __init__(self):
        self.visual_component = None
        self.simulation_core = None
        self.screen_name = None
        self.name = None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100

        self.gateway_addr = "127.0.0.1"
        self.gateway_port = 8081

        self._buffer = []
        self.task_buffer = deque()

        self.network_settings = "tcp:{}:{}".format(
            self.gateway_addr, self.gateway_port)

        # Starts the loop thar will be executed every 1 second to verify if there is tasks in buffer then perform then. - Rafael Sampaio
        LoopingCall(self.compute_core).start(3.0)

    def update_app_name_if_not_exists(self):
        if not self.name and self.visual_component:
            self.name = self.simulation_core.canvas.itemcget(
            self.visual_component.draggable_name, 'text')

    def compute_core(self):
        # Task are given in int MIPS values
        # This simulates compute processor.
        # Here task are performed, then removed from task buffer
        # After perform task and remove from buffer, it sends task result to broker
        # This is called in a looping call, in a discret interval
        # The task MIPS size is wich determines the duration of each loop iteration
        # Rafael Sampaio

        # update component name before use self.name variable - Rafael Sampaio
        self.update_app_name_if_not_exists()

        def perform_next_task_in_buffer(execution_time, task_size, task_id):
            self.simulation_core.updateEventsCounter(self.name+' --> Task '+task_id+' with '+str(task_size)+' MIPS performed in '+str(execution_time)+'s')
            self.send_task_result_to_orchestrator(execution_time, task_size, task_id)

        # if there is tasks in buffer - Rafael Sampaio
        if len(self.task_buffer) > 0:
            # removing task from buffer, buffer size will not be user by controller.
            task = self.task_buffer.popleft()
            task_size = int(task['data']['task'])
            task_id = task['id']

            # getting time in seconds that will be wait for task be performed,
            # this simulates the processor delay - Rafael Sampaio
            schedule_interval = task_size/1000
            reactor.callLater(schedule_interval, perform_next_task_in_buffer,schedule_interval, task_size, task_id)


    def connectionMade(self):
        self.transport.logstr = '-'
        self.screen_name = self.transport.getHost().host+":" + \
            str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(
            self.screen_name+" - Connected to mqtt broker")
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
            "topic": "task",
            "content": "None"
        }

        self.simulation_core.updateEventsCounter(
            self.screen_name+" - sending MQTT SUBSCRIBE REQUEST")
        package = self.build_package(msg, 'mqtt')
        self.send(package)

    def dataReceived(self, data):
        if data.startswith(b'{"destin'):
            if data and data.endswith(b"\n"):
                packages = data.split(b"\n")
                for package in packages:
                    if package != b'':
                        _, _, _, _, _, payload = self.extract_package_contents(package)
                        # prevent the compute node to save packages such as "mqtt ack" to the buffer,
                        # due it dont has any payload with valid data value - Rafael Sampaio
                        if type(payload) == dict:
                            self.task_buffer.append(payload)


    def send_task_result_to_orchestrator(self, execution_time, task_size, task_id):
        # Tells the broker the task result - Rafael Sampaio
        result_msg = {
            "action": "publish",
            "topic": "task_result",
            "content": task_id
        }
        package = self.build_package(result_msg, 'mqtt')
        # Uses commom socket to send mqtt publish message to broker, package format till same twisted - Rafael Sampaio
        s = socket.socket()
        s.connect((self.transport.getPeer().host, self.transport.getPeer().port))
        s.send(package)
        reactor.callLater(2, s.close)
        decripition = (self.name if self.name else str(type(self).__name__))
        self.simulation_core.updateEventsCounter(decripition+' --> Sending task '+task_id+' result to the broker ')


        # falta verificar se o base line performa tarefas primeiro pra depois receber outras
        # falta verificar pq está havendo estouro do limite de portas/sockets - seria o caso de o protocol está sendo persistido pelo lado do broker ao receber uma requisição publish?

class OrchestratorBrokerApp:

    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        broker_factory = OrchestratorBrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text="\n\n\nOrchestrator\n"+str(addr+":"+str(port))) 


class OrchestratorBrokerProtocol(StandardApplicationComponent):

    def __init__(self, factory):
        self.factory = factory
        self.database = False
        self.name = None

    def connectionLost(self, reason):
        try:
            # if self in self.factory.subscribers_dtos:
            #     self.factory.subscribers_dtos.remove(self)
            for dto in self.factory.subscribers_dtos:
                if dto.protocol == self:
                    self.factory.subscribers_dtos.remove(dto)
        except NameError:
            pass

    def connectionMade(self):
        self.visual_component = self.factory.visual_component
        self.simulation_core =  self.factory.simulation_core
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.destiny_addr = self.transport.getPeer().host
        self.destiny_port = self.transport.getPeer().port
        self.transport.logstr = '-'
        response_package = self.build_package("MQTT_ACK", 'mqtt')
        self.send(response_package)
        self.save_protocol_in_simulation_core(self)

        # if the factory aint have a protocol for external connections, this wiil be it - Rafael Sampaio
        # the official protocol is able to forward packets from the factory shared buffer to cloud - Rafael Sampaio
        if not self.factory.official_protocol:
            self.factory.official_protocol = self
            LoopingCall(self.send_task_to_computer_node).start(1.0)

    def send_task_to_computer_node(self):
        # Verify if there is task in buffer - Rafael Sampaio
        if len(self.factory.incoming_buffer) > 0:
        #     verifica qual dos subscribers tem maior capacidade disponivel
        #         verifica se a task tem tamanho em MIPS menor ou igual a disponibilidade do nó com maior capacidade de processamento disponivel
        #             envia a task para o nó com maior capacidade
        #             remove a task do buffer

            # send next task in queue to the computer nodes - Rafael Sampaio
            package = self.factory.incoming_buffer[-1]
            _package = json.loads(package)

            pk = self.build_package(_package, 'mqtt')
            self.send_package_to_all_subscribers(pk)
            self.factory.incoming_buffer.remove(package)

    def send_package_to_all_subscribers(self, package):

        for subscriber in self.factory.subscribers_dtos:
            self.source_addr = subscriber.protocol.transport.getHost().host
            self.source_port = subscriber.protocol.transport.getHost().port
            self.destiny_addr = subscriber.protocol.transport.getPeer().host
            self.destiny_port = subscriber.protocol.transport.getPeer().port
            subscriber.protocol.send(package)

    def dataReceived(self, package):

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
        # Print the received data on the sreen.  - Rafael Sampaio

        action, topic_title, content = extract_mqtt_contents(payload)

        if action == "subscribe":
            # Saving the connected protocol to the factory subscribers protocols list set - Rafael Sampaio
            dto = SubscriberDTO()
            dto.protocol = self
            self.factory.add_subscriber_dto(dto)
            self.send_mqtt_acknowledgement(source_addr, source_port)

        elif action == "publish" and topic_title == 'task':
            # send ack to the sender of the received package - Rafael Sampaio
            self.send_mqtt_acknowledgement(source_addr, source_port)
            if content:
                for measue_values in content:
                    self.factory.incoming_buffer.append(json.dumps(measue_values))

            self.update_last_package_received_time_on_screen()
        else:
            print(action, topic_title, content)
            self.send_mqtt_acknowledgement(source_addr, source_port)

    def send_mqtt_acknowledgement(self, destiny_addr, destiny_port):
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        response_package = self.build_package("MQTT_ACK"+str(uuid.uuid4().fields[-1]), 'mqtt')
        self.send(response_package)
        decripition = (self.name if self.name else str(type(self).__name__))
        self.simulation_core.updateEventsCounter(decripition+' --> Sending acknowledgement to '+str(destiny_addr)+':'+str(destiny_port))

    def update_last_package_received_time_on_screen(self):
        now = datetime.now()
        now = now.strftime("%d/%m/%Y - %H:%M:%S")
        # Printing on the sreen the last time that received any data. - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now+"\n")

    def send(self, message):
        if self.transport:
            self.transport.write(message+b"\n")
        else:
            decripition = (self.name if self.name else str(type(self).__name__))
            log.msg("Info : - | %s - Unknow Device trying to send message, but the protocol is not connected"%decripition)


class OrchestratorBrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers_dtos = []
        self.total_received_bytes = 0

        self.incoming_buffer = []

        # this protocol will be used for send data to the subscribers - Rafael Sampaio
        # it will be the first protocol open by a client connection. - Rafael Sampaio
        # after client connects if this still None the current client connection will be the official protocol - Rafael Sampaio
        self.official_protocol = None

    def add_subscriber_dto(self, dto):
        self.subscribers_dtos.append(dto)

    def remove_subscriber_dto_by_addr_and_port_string(self, dto):
        self.subscribers_dtos.remove(dto)

    def buildProtocol(self, addr):
        return OrchestratorBrokerProtocol(self)


class SubscriberDTO(object):
    def __init__(self) -> None:
        self.running_tasks = []
        self.performed_tasks = []
        self.protocol = None
        self.status = "idle" # can be idle or busy - Rafael Sampaio
        self.initial_capacity = DEFAULT_FOG_NODE_MIPS_CAPACITY
        self.atual_capacity = self.initial_capacity

    def toogle_status(self):
        if self.status == "idle":
            self.status = "busy"
        else:
            self.status = "idle"

    def increase_capacity(self, task_size):
        self.atual_capacity = self.atual_capacity+task_size

    def decrease_capacity(self, task_size):
        self.atual_capacity = self.atual_capacity-task_size



MQTT_ACK = {"action": "response", "topic": "any", "content": "MQTT_ACK"}
