from platform import machine
import uuid
from core.functions import import_and_instantiate_class_from_string
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName
import tkinter as tk

class Machine(object):
    def __init__(
            self,
            simulation_core,
            name,
            ip,
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
        self.ip = ip
        self.type = type
        self.app = import_and_instantiate_class_from_string(app)
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, coverage_area_radius, self)
        self.peers = []
        self.links = []
        
        self.app.simulation_core = simulation_core
        self.app.machine = self

    def turn_on(self):
        self.simulation_core.updateEventsCounter(f"Info : - | {self.name} - Initializing machine")
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
                self.simulation_core.all_links.append(_link)
                self.links.append(_link)
                _link.draw_connection_arrow()
            else:
                self.simulation_core.updateEventsCounter(f"Info : - | {self.name} - Already connected to {peer_address}")
            
    def verify_if_connection_link_already_exists(self, machine):
        return next(filter(lambda link: link.machine_1 == machine or link.machine_2 == machine,  self.links), None)
        
class Link(object):
    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = 'LAN'
        self.is_wireless = False
        self.bandwidth = '256kbps'
        self.latency = '0.02s'
        self.packet_loss_percentage = 10
        self.machine_1 = None
        self.machine_2 = None
        self.packets_queue =  []
        self.connection_arrow = None

    def handle_packet(self):
        pass
    
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
        self.simulation_core.updateEventsCounter(f"Info : - | {self.name} - Connecting {self.machine_1.ip} to {self.machine_2.ip}")
    
class FogWirelessLink(Link):
    def __init__(self, simulation_core):
        super(FogWirelessLink, self).__init__(simulation_core)
        self.name = 'Fog Local Network'
        self.is_wireless = True
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
        self.id = uuid.uuid4().hex
        self.MIPS = MIPS
        self.source_addr = source_addr
        self.source_port = source_port
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.payload = payload
        self.trace = []