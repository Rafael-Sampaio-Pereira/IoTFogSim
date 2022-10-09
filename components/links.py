import uuid
from core.engine.network import drop_packet, simulate_network_delay
from twisted.python import log
from twisted.internet.task import LoopingCall
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet import reactor
        
        
class Link(object):
    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().fields[-1]
        self.name = f'Link {self.id}'
        self.bandwidth = 256 #kbps
        self.packet_loss_rate = 0.5
        self.network_interface_1 = None
        self.network_interface_2 = None
        self.packets_queue =  []
        self.connection_arrow = None
        self.sent_packets = []
        self.dropped_packets = []
        self.all_delays = []
        self.delay_upper_bound = None
        self.delay_lower_bound = None
        self.delay_mean = None
        self.delay_standard_deviation = None
        LoopingCall(self.transmission_channel).start(0.001) # fast as can be o prevent false delay on packet delivery
        
    def transmission_channel(self):
        self.handle_packets()

    def handle_packets(self):
        if len(self.packets_queue) > 0:
            for packet in self.packets_queue.copy():
                sender = packet.trace[-1]

                if not drop_packet(self.packet_loss_rate, self.simulation_core.global_seed):
                    delay = simulate_network_delay(
                        self.delay_upper_bound,
                        self.delay_lower_bound,
                        self.delay_mean,
                        self.delay_standard_deviation
                    )
                    self.all_delays.append(delay)
                    self.sent_packets.append(packet)
                    if sender == self.network_interface_1:
                        self.animate_package(packet)
                        packet.trace.append(self.network_interface_2)
                        reactor.callLater(delay, self.network_interface_2.machine.app.in_buffer.append, packet)
                        self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id} delay {delay}ms")
                    elif sender == self.network_interface_2:
                        self.animate_package(packet)
                        packet.trace.append(self.network_interface_1)
                        reactor.callLater(delay, self.network_interface_1.machine.app.in_buffer.append, packet)
                        self.simulation_core.updateEventsCounter(f"{self.name} - Transmiting packet {packet.id} delay {delay}ms")
                    
                    self.packets_queue.remove(packet)
                else:
                    self.dropped_packets.append(packet)
                    self.simulation_core.updateEventsCounter(f"{self.name} - Failed to transmiting packet {packet.id}. Packet was dropped")
                    if sender.machine.app.protocol == 'TCP':
                        log.msg(f"Info :  - | {self.name} - Packet {packet.id} will be retransmitted due sender protocol is TCP")
                    else:
                        # if sender app protocol is not tcp, it will drop the packet and don't care about retransmissions
                        self.packets_queue.remove(packet)


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
