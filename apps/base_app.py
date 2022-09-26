import uuid
from core.components import Packet
from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet.task import LoopingCall

DEFAULT_MIPS = 1025
class BaseApp(object):
    def __init__(self):
        self.simulation_core = None
        self.id = uuid.uuid4().hex
        self.name = 'my_app'
        self.port = 8081
        self.protocol = 'TCP' # can be UDP or TCP must implements enum
        self.machine = None
        self.in_buffer = []

    def main(self):
        pass
    
    @inlineCallbacks 
    def start(self):
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Initializing app")
        yield sleep(0.5)
        self.main()

    def send_packet(self, destiny_addr, destiny_port, payload, MIPS):
        _packet = Packet(
            self.simulation_core,
            self.machine.network_interfaces[0].ip,
            self.port,
            destiny_addr,
            destiny_port,
            payload,
            MIPS
        )
        _packet.trace.append(self)
        self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.network_interfaces[0].ip}) creating packet {_packet.id}")
        if len(self.machine.links) > 0:
            self.machine.links[0].packets_queue.append(_packet)
            self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.network_interfaces[0].ip}) sending packet {_packet.id} to {destiny_addr}")
        else:
            log.msg(f"Info : - | {self.machine.type}({self.machine.network_interfaces[0].ip}) are not connected to a peer. Packet {_packet.id} can not be sent")

class SimpleWebClientApp(BaseApp):

    def __init__(self):
        super(SimpleWebClientApp, self).__init__()
        self.port = 80
        self.name ='WEBClient'
    
    def main(self):
        super().main()
        self.machine.connect_to_peer('192.168.0.1')
        self.send_packet(
            '192.168.0.3',
            80,
            'HTTP 1.0 POST request',
            DEFAULT_MIPS
        )
        LoopingCall(self.main_loop).start(0.1)
        
    def main_loop(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id} with {packet.MIPS} MIPS. Payload: {packet.payload}")
                self.in_buffer.remove(packet)
                
class SimpleWebServerApp(BaseApp):
    def __init__(self):
        super(SimpleWebServerApp, self).__init__()
        self.port = 80
        self.name ='WEBServer'
    
    def main_loop(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id} with {packet.MIPS} MIPS. Payload: {packet.payload}")
                self.in_buffer.remove(packet)
                self.send_http_200_response(packet.source_addr, packet.source_port, 'HTTP 1.0 response', DEFAULT_MIPS)
        
    def send_http_200_response(self, destiny_addr, destiny_port, response,  MIPS):
        self.send_packet(
            destiny_addr,
            destiny_port,
            response,
            MIPS
        )

    def main(self):
        super().main()
        self.machine.connect_to_peer('192.168.0.1')
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Start listen on port {self.port}")
        LoopingCall(self.main_loop).start(0.1)

class RouterApp(BaseApp):
    def __init__(self):
        super(RouterApp, self).__init__()
        self.protocol = 'TCP'

    def main_loop(self):
        
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                destiny = self.simulation_core.get_machine_by_ip(packet.destiny_addr)
                
                # verify if destiny is connected peers list, link in ip routering table
                if destiny and destiny in self.machine.peers:
                    self.direct_forward_packet(packet, destiny)
                
                #se não estiver, descarta o pacote
                self.in_buffer.remove(packet)
        
    def main(self):
        super().main()
        LoopingCall(self.main_loop).start(0.1)
        
    def direct_forward_packet(self, packet, destiny):
        destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
        destiny_link.packets_queue.append(packet)
        
    # def connect_to_another_network(self, network_gateway_address):
    #     # verify if there is a machine in simulation_core with this address
    #     neighbor_gateway = self.simulation_core.get_machine_by_ip(peer_address)
    #     if peer:
    #         # verify if there is already a connection between the peer and the source
    #         if not self.verify_if_connection_link_already_exists(peer):
    #             _link = FogWirelessLink(self.simulation_core)
    #             _link.machine_1 = self
    #             _link.machine_2 = peer
    #             peer.peers.append(self)
    #             self.peers.append(peer)
    #             self.simulation_core.all_links.append(_link)
    #             self.links.append(_link)
    #             peer.links.append(_link)
    #             _link.draw_connection_arrow()
    #         else:
    #             log.msg(f"Info : - | {self.name}-{self.type} - Already connected to {peer_address}")
        
class AccessPointApp(RouterApp):
    def __init__(self):
        super(AccessPointApp, self).__init__() 