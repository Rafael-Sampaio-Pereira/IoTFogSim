import datetime
import uuid
from core.functions import import_and_instantiate_class_from_string
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName
from core.engine.network import drop_packet
import tkinter as tk
from twisted.python import log
from twisted.internet.task import LoopingCall
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep


class NetworkInterface(object):
    def __init__(self, simulation_core, name, is_wireless, ip, machine):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.is_wireless = is_wireless
        self.ip = ip
        self.machine = machine
        
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
            coverage_area_radius,
            connected_gateway_addrs
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
        self.network_interfaces = []
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, coverage_area_radius, self)
        self.peers = []
        self.links = []
        self.connected_gateway_addrs = connected_gateway_addrs
        self.app.simulation_core = simulation_core
        self.app.machine = self
        
    
    @inlineCallbacks
    def propagate_signal(self):
        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline="red")

        for n in range(0, self.visual_component.coverage_area_radius):
            # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
            if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
                # the ssignal radius propagates at 1 units per time. - Rafael Sampaio
                self.visual_component.signal_radius += 2
                self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y +
                                                   self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            else:
                # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
                self.simulation_core.canvas.itemconfig(
                    self.visual_component.draggable_signal_circle, outline="")
                self.visual_component.signal_radius = 1
                self.simulation_core.canvas.update()
            yield sleep(0.001)
        

    def turn_on(self):
        self.simulation_core.updateEventsCounter(f"{self.name} - Initializing {self.type}...")
        self.update_name_on_screen(self.name+'\n'+self.network_interfaces[0].ip)
        self.app.start()
    
    def connect_to_peer(self, peer_address):
        # verify if there is a machine in simulation_core with this address
        peer = self.simulation_core.get_machine_by_ip(peer_address)
        if peer:
            # verify if there is already a connection between the peer and the source
            if not self.verify_if_connection_link_already_exists(peer):
                _link = FogWirelessLink(self.simulation_core)
                _link.network_interface_1 = self.network_interfaces[0]
                _link.network_interface_2 = peer.network_interfaces[0]
                peer.peers.append(self)
                self.peers.append(peer)
                self.simulation_core.all_links.append(_link)
                self.links.append(_link)
                peer.links.append(_link)
                _link.draw_connection_arrow()
            else:
                log.msg(f"Info :  - | {self.name}-{self.type} - Already connected to {peer_address}")
            
    def verify_if_connection_link_already_exists(self, machine):
        """Verify if connection link already exists, if exists returns it"""
        return next(filter(lambda link: link.network_interface_1.machine == machine or link.network_interface_2.machine == machine,  self.links), None)
    
    def update_name_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(msg))
        
class Link(object):
    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().fields[-1]
        self.name = f'Link {self.id}'
        self.bandwidth = '256kbps'
        self.latency = '0.02s'
        self.packet_loss_rate = 0.5
        self.network_interface_1 = None
        self.network_interface_2 = None
        self.packets_queue =  []
        self.connection_arrow = None
        LoopingCall(self.transmission_channel).start(0.1)
        
    def transmission_channel(self):
        # HERE NEEDS TO IMPLEMENTATION OF THE LATENCY
        self.handle_packets()

    def handle_packets(self):
        if len(self.packets_queue) > 0:
            for packet in self.packets_queue.copy():
                sender = packet.trace[-1]
                if not drop_packet(self.packet_loss_rate, self.simulation_core.global_seed):
                    if sender == self.network_interface_1:
                        self.animate_package(packet)
                        packet.trace.append(self.network_interface_2)
                        self.network_interface_2.machine.app.in_buffer.append(packet)
                        self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id}")
                    elif sender == self.network_interface_2:
                        self.animate_package(packet)
                        packet.trace.append(self.network_interface_1)
                        self.network_interface_1.machine.app.in_buffer.append(packet)
                        self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id}")
                    
                    self.packets_queue.remove(packet)
                else:
                    self.simulation_core.updateEventsCounter(f"{self.name} - Failed to transmiting packet {packet.id}. Packet was dropped")
                    if sender.machine.app.protocol == 'TCP':
                        log.msg(f"Info :  - | {self.name} - Packet {packet.id} will be retransmitted due sender protocol is TCP")
                    else:
                        # if sender app protocol is not tcp, it will drop the packet and don't care about retransmissions
                        self.packets_queue.remove(packet)
                        print("Não vai reenviar", sender.machine.app.protocol)

    def draw_connection_arrow(self):
        self.connection_arrow = self.simulation_core.canvas.create_line(
            self.network_interface_1.machine.visual_component.x,
            self.network_interface_1.machine.visual_component.y,
            self.network_interface_2.machine.visual_component.x,
            self.network_interface_2.machine.visual_component.y,
            arrow="both",
            width=1,
            dash=(4,2)
        )
        self.simulation_core.updateEventsCounter(f"{self.name} - {self.network_interface_1.machine.type}({self.network_interface_1.ip})\u27F5 \u27F6  ({self.network_interface_2.ip}){self.network_interface_2.machine.type}")
    
    def animate_package(self, packet):
        # by looking for last machine in packet trace we can find the sender
        if len(packet.trace) > 0:
            sender = packet.trace[-1]
            receiver = None
            
            if sender == self.network_interface_1:
                receiver = self.network_interface_2
            elif sender == self.network_interface_2:
                receiver = self.network_interface_1

            x1 = sender.machine.visual_component.x
            y1 = sender.machine.visual_component.y
            x2 = receiver.machine.visual_component.x
            y2 = receiver.machine.visual_component.y
                    
            self.ball = self.simulation_core.canvas.create_oval(
                x1, y1, x1+7, y1+7, fill="red"
            )
            self.all_coordinates = list(bresenham(
                x1, y1, x2, y2
            ))
            self.display_time = 9 # time that the packege ball still on the screen after get the destinantion - Rafael Sampaio
            self.package_speed = 1 # this must be interger and determines the velocity of the packet moving in the canvas - Rafael Sampaio

            cont = 100
            for x, y in self.all_coordinates:
                # verify if package ball just got its destiny - Rafael Sampaio
                if x == x2 and y == y2:
                    self.simulation_core.canvas.after(cont+self.display_time,self.simulation_core.canvas.delete, self.ball)

                self.simulation_core.canvas.after(cont, self.simulation_core.canvas.coords, self.ball, x, y, x+7, y+7) # 7 is the package ball size - Rafael Sampaio
                cont = cont + self.package_speed
    
class FogWirelessLink(Link):
    def __init__(self, simulation_core):
        super(FogWirelessLink, self).__init__(simulation_core)
        self.bandwidth = '256kbps'
        self.latency = '0.02s'
        self.packet_loss_rate = 0.10
        

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