import datetime
import uuid
from core.functions import import_and_instantiate_class_from_string
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName
import tkinter as tk
from twisted.python import log
from twisted.internet.task import LoopingCall

class NetworkInterface(object):
    def __init__(self, simulation_core, name, is_wireless, ip):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.is_wireless = is_wireless
        self.ip = ip
        
class Machine(object):
    def __init__(
            self,
            simulation_core,
            name,
            MIPS,
            icon,
            is_wireless,
            x,
            y,
            app,
            type,
            coverage_area_radius
        ):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.MIPS = MIPS
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file
        self.is_wireless = is_wireless
        self.type = type
        self.app = import_and_instantiate_class_from_string(app)
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, coverage_area_radius, self)
        self.peers = []
        
        self.network_interfaces = []
        self.links = []
        
        self.app.simulation_core = simulation_core
        self.app.machine = self

    def turn_on(self):
        self.simulation_core.updateEventsCounter(f"{self.name} - Initializing {self.type}")
        self.app.start()
    
    def connect_to_peer(self, peer_address):
        # verify if there is a machine in simulation_core with this address
        peer = self.simulation_core.get_machine_by_ip(peer_address)
        if peer:
            # verify if there is already a connection between the peer and the source
            if not self.verify_if_connection_link_already_exists(peer):
                _link = FogWirelessLink(self.simulation_core)
                _link.machine_1 = self
                _link.machine_2 = peer
                peer.peers.append(self)
                self.peers.append(peer)
                self.simulation_core.all_links.append(_link)
                self.links.append(_link)
                peer.links.append(_link)
                _link.draw_connection_arrow()
            else:
                log.msg(f"Info : - | {self.name}-{self.type} - Already connected to {peer_address}")
            
    def verify_if_connection_link_already_exists(self, machine):
        """Verify if connection link already exists, if exists returns it"""
        return next(filter(lambda link: link.machine_1 == machine or link.machine_2 == machine,  self.links), None)
        
class Link(object):
    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = f'Link {self.id}'
        self.bandwidth = '256kbps'
        self.latency = '0.02s'
        self.packet_loss_percentage = 10
        self.machine_1 = None
        self.machine_2 = None
        self.packets_queue =  []
        self.connection_arrow = None
        LoopingCall(self.transmission_channel).start(0.1)
        
    def transmission_channel(self):
        # HERE NEEDS TO IMPLEMENTATION OF THE LATENCY, PACKET LOSS
        self.handle_packets()

    def handle_packets(self):
        if len(self.packets_queue) > 0:
            for packet in self.packets_queue.copy():
                source = self.simulation_core.get_machine_by_ip(packet.source_addr)
                if source == self.machine_1:
                    packet.trace.append(self.machine_2)
                    self.machine_2.app.in_buffer.append(packet)
                    self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id} from {self.machine_1.type}({self.machine_1.network_interfaces[0].ip}) to {self.machine_2.type}({self.machine_2.network_interfaces[0].ip})")
                else:
                    packet.trace.append(self.machine_1)
                    self.machine_1.app.in_buffer.append(packet)
                    self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id} from {self.machine_2.type}({self.machine_2.network_interfaces[0].ip}) to {self.machine_1.type}({self.machine_1.network_interfaces[0].ip})")
                self.packets_queue.remove(packet)
    
    def draw_connection_arrow(self):
        self.connection_arrow = self.simulation_core.canvas.create_line(
            self.machine_1.visual_component.x,
            self.machine_1.visual_component.y,
            self.machine_2.visual_component.x,
            self.machine_2.visual_component.y,
            arrow="both",
            width=1,
            dash=(4,2)
        )
        self.simulation_core.updateEventsCounter(f"{self.name} - Connecting {self.machine_1.type}({self.machine_1.network_interfaces[0].ip}) to {self.machine_2.type}({self.machine_2.network_interfaces[0].ip})")
    
class FogWirelessLink(Link):
    def __init__(self, simulation_core):
        super(FogWirelessLink, self).__init__(simulation_core)
        self.bandwidth = '256kbps'
        self.latency = '0.02s'
        self.packet_loss_percentage = 10

class Packet(object):
    def __init__(
            self,
            simulation_core,
            source_addr,
            source_port,
            destiny_addr,
            destiny_port,
            payload,
            MIPS
        ):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().fields[-1]
        self.MIPS = MIPS
        self.source_addr = source_addr
        self.source_port = source_port
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.payload = payload
        self.trace = []
        self.created_at = datetime.datetime.now().isoformat()