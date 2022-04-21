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
from operator import attrgetter

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
            self.name = self.visual_component.deviceName

    def compute_core(self):
        # Task are given in int MIPS values
        # This simulates compute processor.
        # Here task are performed, then removed from task buffer
        # After perform task and remove from buffer, it sends task result to broker
        # This is called in a looping call, in a discret interval
        # The task MIPS size is wich determines the duration of each loop iteration
        # Rafael Sampaio

        def perform_next_task_in_buffer(execution_time, task):
            task_size = int(task['data']['task'])
            self.simulation_core.updateEventsCounter(self.visual_component.deviceName+' --> Task '+task['id']+' with '+str(task_size)+' MIPS performed in '+str(execution_time)+'s')
            task['execution_time'] = execution_time
            task['performed_at'] = datetime.now().isoformat()
            self.send_task_result_to_orchestrator(task)

        # if there is tasks in buffer - Rafael Sampaio
        if len(self.task_buffer) > 0:
            # removing task from buffer, buffer size will not be user by controller.
            task = self.task_buffer.popleft()

            # getting time in seconds that will be wait for task be performed,
            # this simulates the processor delay - Rafael Sampaio
            schedule_interval = int(task['data']['task'])/1000
            reactor.callLater(schedule_interval, perform_next_task_in_buffer,schedule_interval, task)


    def connectionMade(self):
        self.transport.logstr = '-'
        self.screen_name = "\n\n"+self.visual_component.deviceName+"\n   "+self.transport.getHost().host+":" + \
            str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(
            self.visual_component.deviceName+" - Connected to mqtt broker")
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
            self.visual_component.deviceName+" - Sending MQTT subscribe request")
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


    def send_task_result_to_orchestrator(self, task):
        # Tells the broker the task result - Rafael Sampaio
        result_msg = {
            "action": "publish",
            "topic": "task_result",
            "content": task
        }
        package = self.build_package(result_msg, 'mqtt')
        # Uses commom socket to send mqtt publish message to broker, package format till same twisted - Rafael Sampaio
        s = socket.socket()
        s.connect((self.transport.getPeer().host, self.transport.getPeer().port))
        s.send(package)
        reactor.callLater(2, s.close)
        decripition = (self.visual_component.deviceName  if self.visual_component.deviceName else str(type(self).__name__))
        self.simulation_core.updateEventsCounter(decripition+' --> Sending task '+task['id']+' result to the broker ')

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
            for dto in self.factory.subscribers_dtos:
                if dto.protocol == self:
                    log.msg("Info : - | A subscribed device lose it connection to the Broker")
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
            # Verify if there is some compute node in subscribers list - Rafael Sampaio
            if len(self.factory.subscribers_dtos) > 0:
                # Getting the compute node in fog that is the greater capacity node - Rafael Sampaio
                greater_capacity_node_dto = max(self.factory.subscribers_dtos.copy(), key=attrgetter('atual_capacity'))

                # getting next task in queue - Rafael Sampaio
                package = self.factory.incoming_buffer[-1]
                _package = json.loads(package)
                task_size = int(_package['data']['task'])
                # Verify if next task size is less than equals to the compute node atual capacity - Rafael Sampaio
                if task_size <= greater_capacity_node_dto.atual_capacity:
                    pk = self.build_package(_package, 'mqtt')
                    self.send_package_to_one_subscriber(pk, greater_capacity_node_dto)
                    # after send, remove task  from buffer - Rafael Sampaio
                    self.factory.incoming_buffer.remove(package)
                    # Adds the task to the running tasks list of the compute node - Rafal Sampaio
                    greater_capacity_node_dto.running_tasks.append(_package)
                    # subtracts the size of the task from the total size of the current computational capacity of the node - Rafael Sampaio
                    greater_capacity_node_dto.decrease_capacity(task_size)
                    destiny_as_string = greater_capacity_node_dto.protocol.destiny_addr+":"+str(greater_capacity_node_dto.protocol.destiny_port)
                    self.simulation_core.updateEventsCounter(self.visual_component.deviceName+' --> Sending task %s to compute node %s at Fog tier'%(_package['id'], destiny_as_string))

    def send_package_to_all_subscribers(self, package):
        for subscriber in self.factory.subscribers_dtos:
            self.source_addr = subscriber.protocol.transport.getHost().host
            self.source_port = subscriber.protocol.transport.getHost().port
            self.destiny_addr = subscriber.protocol.transport.getPeer().host
            self.destiny_port = subscriber.protocol.transport.getPeer().port
            subscriber.protocol.send(package)

    def send_package_to_one_subscriber(self, package, dto):
        self.source_addr = dto.protocol.transport.getHost().host
        self.source_port = dto.protocol.transport.getHost().port
        self.destiny_addr = dto.protocol.transport.getPeer().host
        self.destiny_port = dto.protocol.transport.getPeer().port
        dto.protocol.send(package)

    def dataReceived(self, package):

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)

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
                    decripition = (self.visual_component.deviceName  if self.visual_component.deviceName else str(type(self).__name__))
                    self.simulation_core.updateEventsCounter(decripition+' --> Storing task %s in Broker buffer queue'%measue_values['id'])
                    self.factory.incoming_buffer.append(json.dumps(measue_values))
            self.update_last_package_received_time_on_screen()

        elif action == "publish" and topic_title == 'task_result':
            self.simulation_core.updateEventsCounter(self.visual_component.deviceName+' --> Received task %s result from compute node at Fog tier'%content['id'])
            dto = self.get_subscriber_dto_by_task_id(content['id'])
            # Giving back the capacity used to perform taks - Rafael Sampaio
            dto.increase_capacity(int(content['data']['task']))

            # Saving the performed task to the performed tasks list of the dto - Rafael Sampaio
            dto.performed_tasks.append(content)

            # Removing perfomed task from running tasks list of the dto - Rafael Sampaio
            to_be_removed = next((i for i in dto.running_tasks if i['id'] == content['id']), None)
            if to_be_removed:
                dto.running_tasks.remove(to_be_removed)
            self.send_mqtt_acknowledgement(source_addr, source_port)

    def get_subscriber_dto_by_task_id(self, task_id):
        # This returns a dto that have task id in running tasks list - Rafael Sampaio
        def second_level_search_get_task_by_id(task_id, task_list):
            task = next((i for i in task_list if i['id'] == task_id), None)
            return task if task else {"id": None} # If task not found in current checked dto, just returns a empty struct - Rafael Sampaio

        dto = next((i for i in self.factory.subscribers_dtos.copy() if (task_id == second_level_search_get_task_by_id(task_id, i.running_tasks.copy())['id'])), None)
        return dto

    def send_mqtt_acknowledgement(self, destiny_addr, destiny_port):
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        response_package = self.build_package("MQTT_ACK"+str(uuid.uuid4().fields[-1]), 'mqtt')
        self.send(response_package)
        decripition = (self.visual_component.deviceName  if self.visual_component.deviceName else str(type(self).__name__))
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
            decripition = (self.visual_component.deviceName  if self.visual_component.deviceName else str(type(self).__name__))
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
    """
        This is just a Data Transfer Object
        This contols task life cicles
        This stores the states of the compute node subscribed
    """
    def __init__(self) -> None:
        self.running_tasks = []
        self.performed_tasks = []
        self.protocol = None
        self.initial_capacity = DEFAULT_FOG_NODE_MIPS_CAPACITY
        self.atual_capacity = self.initial_capacity

    def increase_capacity(self, task_size):
        self.atual_capacity = self.atual_capacity+task_size

    def decrease_capacity(self, task_size):
        self.atual_capacity = self.atual_capacity-task_size


MQTT_ACK = {"action": "response", "topic": "any", "content": "MQTT_ACK"}
