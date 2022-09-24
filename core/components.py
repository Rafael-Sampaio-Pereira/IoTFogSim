import uuid
from core.functions import import_and_instantiate_class_from_string
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName


class IPV6Manager(object):
    def __init__(self, simulation_core):
        self.all_ipv6 = set()

class Link(object):
    def __init__(
            self,
            simulation_core,
            name,
            bandwidth,
            latency,
            machine_1,
            machine_2,
            protocol,
            packet_loss_percentage,
            is_wireless = False
        ):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.is_wireless = is_wireless
        self.bandwidth = bandwidth
        self.latency = latency
        self.machine_1 = machine_1
        self.machine_2 = machine_2
        self.protocol = protocol
        self.packets_queue =  set()
        self.connection_arrow = None

    def handle_packet(self):
        pass

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
        self.ipv6 = "ipv6"
        self.type = type
        self.app = import_and_instantiate_class_from_string(app)
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, coverage_area_radius, self)
        self.peers = set()
        self.links = set()
        
        self.app.simulation_core = simulation_core
        self.app.machine = self
        
        self.turn_on()
        
    def turn_on(self):
        self.simulation_core.updateEventsCounter(f"Info : - | {self.name} - Initializing machine.")
        self.app.start()
    
    def connect_to_peer(self):
        pass

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
        self.trace = set()