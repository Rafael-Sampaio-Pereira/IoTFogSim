import datetime
import uuid
from components.packets import Packet
from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import os


class BaseApp(object):
    def __init__(self):
        self.simulation_core = None
        self.id = uuid.uuid4().hex
        self.name = 'BaseApp'
        self.port = 8081
        self.protocol = 'TCP' # can be UDP or TCP must implements enum
        self.machine = None
        self.in_buffer = []
        self.is_running = False
        self.dataset_file = None
        self.last_actor = 'Unknow' # Last person/system that has interacted with the app
        self.dataset_file_has_header = False
        
    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (Kw); last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())
        
    def check_in_buffer(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                self.in_buffer.remove(packet)
                del packet

    def main(self):
        # create results directoy if it not exist
        os.makedirs(self.simulation_core.output_dir+"/datasets/", exist_ok=True)
        file = self.simulation_core.output_dir+"/datasets/" + \
            self.simulation_core.project_name+"_"+self.machine.name+".csv"
        self.dataset_file  = open(file, 'a')
        if self.machine.is_turned_on:
            LoopingCall(self.update_dataset).start(interval=self.simulation_core.clock.get_internal_time_unit(1), now=True)
            LoopingCall(self.measure_energy).start(interval=self.simulation_core.clock.get_internal_time_unit(1), now=True)

    def measure_energy(self):
        if self.machine.is_turned_on:
            self.simulation_core.smart_energy_meter.app.mesure_energy(
                round(self.machine.current_consumption,3)
            )

    def set_simulation_core(self, simulation_core):
        self.simulation_core = simulation_core
    
    @inlineCallbacks 
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Starting app...")
            yield sleep(0.5)
            reactor.callFromThread(self.main)

    def send_packet(
        self, destiny_addr, destiny_port, payload, length, last_link=None, color=None, network_interface_indice=0):
        """ Send a packet. Use last_link parameter to send back a response
            using same link/connection that has been used to receive the
            request packet
        """
        _packet = Packet(
            self.simulation_core,
            self.machine.network_interfaces[network_interface_indice].ip,
            self.port,
            destiny_addr,
            destiny_port,
            payload,
            length,
            color= color or None
        )
        _packet.trace.append(self.machine.network_interfaces[network_interface_indice])
        self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.network_interfaces[network_interface_indice].ip}) creating packet {_packet.id} with {length}")
        if len(self.machine.links) > 0:
            peer = None
            if self.machine.network_interfaces[network_interface_indice].is_wireless:
                reactor.callFromThread(self.machine.propagate_signal)

            # Used for send response back to origin peer with same used link
            if last_link:
                last_link.packets_queue.append(_packet)
                if self.machine.network_interfaces[network_interface_indice] != last_link.network_interface_1:
                    peer=last_link.network_interface_1
                else:
                    peer=last_link.network_interface_2
            
            # Used when is starting a new conversation
            else:
                self.machine.links[network_interface_indice].packets_queue.append(_packet)
                if self.machine.network_interfaces[network_interface_indice] != self.machine.links[network_interface_indice].network_interface_1:
                    peer=self.machine.links[network_interface_indice].network_interface_1
                else:
                    peer=self.machine.links[network_interface_indice].network_interface_2
                    
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[network_interface_indice].ip} \u27FC   \u2344 \u27F6  {peer.ip} - packet: {_packet.id}")
        else:
            log.msg(f"Info :  - | {self.machine.type}({self.machine.network_interfaces[network_interface_indice].ip}) are not connected to a peer. Packet {_packet.id} can not be sent")
