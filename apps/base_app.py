import uuid
from core.components import Packet, FogWirelessLink
from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet.task import LoopingCall
from core.engine.network import extract_ip_prefix


DEFAULT_MIPS = 1024
class BaseApp(object):
    def __init__(self):
        self.simulation_core = None
        self.id = uuid.uuid4().hex
        self.name = 'BaseApp'
        self.port = 8081
        self.protocol = 'TCP' # can be UDP or TCP must implements enum
        self.machine = None
        self.in_buffer = []

    def main(self):
        pass
    
    @inlineCallbacks 
    def start(self):
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Starting app...")
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
        _packet.trace.append(self.machine.network_interfaces[0])
        self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.network_interfaces[0].ip}) creating packet {_packet.id}")
        if len(self.machine.links) > 0:
            self.machine.links[0].packets_queue.append(_packet)
            peer = None
            if self.machine.network_interfaces[0] != self.machine.links[0].network_interface_1:
                peer=self.machine.links[0].network_interface_1
            else:
                peer=self.machine.links[0].network_interface_2
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[0].ip} \u27FC   \u2344 \u27F6  {peer.ip} - packet: {_packet.id}")
        else:
            log.msg(f"Info :  - | {self.machine.type}({self.machine.network_interfaces[0].ip}) are not connected to a peer. Packet {_packet.id} can not be sent")

class SimpleWebClientApp(BaseApp):

    def __init__(self):
        super(SimpleWebClientApp, self).__init__()
        self.port = 80
        self.name ='WEBClient'
        
        
    def main(self):
        super().main()
        self.machine.connect_to_peer(self.machine.connected_gateway_addrs[0])
        self.send_packet(
            '192.168.1.2',
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
                if packet.destiny_port == self.port:
                    self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id} with {packet.MIPS} MIPS. Payload: {packet.payload}")
                    self.in_buffer.remove(packet)
                    self.send_http_200_response(packet.source_addr, packet.source_port, 'HTTP 1.0 response', DEFAULT_MIPS)
                else:
                    self.in_buffer.remove(packet)
                    self.send_http_404_response(packet.source_addr, packet.source_port, DEFAULT_MIPS)
                    
        
    def send_http_200_response(self, destiny_addr, destiny_port, response,  MIPS):
        self.send_packet(
            destiny_addr,
            destiny_port,
            response,
            MIPS
        )
        
    def send_http_404_response(self, destiny_addr, destiny_port, MIPS):
        self.send_packet(
            destiny_addr,
            destiny_port,
            'HTTP 1.0 404 - NOT FOUND',
            MIPS
        )

    def main(self):
        super().main()
        self.machine.connect_to_peer(self.machine.connected_gateway_addrs[0])
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Start listen on port {self.port}")
        LoopingCall(self.main_loop).start(0.1)

class RouterApp(BaseApp):
    def __init__(self):
        super(RouterApp, self).__init__()
        self.protocol = 'TCP'
        self.neighbor_gateways = []
        self.name = f'RouterApp'
        
        
    def find_route_hops(self, gateway, packet, destiny_addr_prefix):
        """
        Esta função utiliza a busca em largura para encontrar quais os saltos (gateways)
        que estão no caminho entre duas redes, isto é, quando um gateway(i.e. roteador ou switch)
        encontram um ip com prefixo desconhecido, ou seja, que não está na mesma rede que ele (utilizando a network_interfaces[0])
        ele procura através dos gateways vizinhos (utilizando a network_interfaces[1]) quem porventura conhece aquele prefixo.
        Quando o prefixo desejado é encontrado, o próximo salto na rota até ele é retornado em uma lista, se o prefixo desejado
        não for encontrado, retorna uma lista vazia.
        """
        
        visited=[]
        queue=[]
        visited.append(gateway)
        queue.append(gateway)
        route=[]
        
        while queue:
            
            current_gateway=queue.pop(0)
            
            for neighbor_gateway in current_gateway.app.neighbor_gateways:
                
                if neighbor_gateway not in visited:
                    visited.append(neighbor_gateway)
                    queue.append(neighbor_gateway)
                    
                    if neighbor_gateway.network_interfaces[1] not in packet.trace:
                        if current_gateway.network_interfaces[1] not in packet.trace:
                            route.append(current_gateway)
                        else:
                            route.append(neighbor_gateway)
                        if neighbor_gateway.network_interfaces[0].ip.startswith(destiny_addr_prefix):
                            return route
            
            route = []
                            
        return []
    
    
    
    

    def main_loop(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                destiny = self.simulation_core.get_machine_by_ip(packet.destiny_addr)
                # verify if destiny is connected peers list, link in ip routering table
                if destiny and destiny in self.machine.peers:
                    packet.trace.append(self.machine.network_interfaces[0])
                    self.direct_forward_packet(packet, destiny)
                # if are not connected to destiny, try to find a route and send the packet
                else:
                    packet.trace.append(self.machine.network_interfaces[1])
                    destiny_addr_prefix = extract_ip_prefix(packet.destiny_addr)
                    route_hops = self.find_route_hops(self.machine, packet, destiny_addr_prefix)
                    
                    # if there is hops, we can send the packet to the first hop in the list
                    if route_hops:
                        if len(route_hops) > 0 :
                            self.forward_packet_to_another_gateway(packet, route_hops[0])
                    else:
                        log.msg(f"Info :  - | {self.machine.type}({self.machine.network_interfaces[1].ip}) could not find a route to {destiny_addr_prefix} subnetwork")
                
                # if are not connected to destiny
                # or dont found any route to forward packets,
                # or packet was successfully forwarded
                # just drop packets from in_buffer
                self.in_buffer.remove(packet)
                        
    def main(self):
        super().main()
        for gtw_addr in self.machine.connected_gateway_addrs:
            self.connect_to_another_network(gtw_addr)
        LoopingCall(self.main_loop).start(0.1)
        
    def direct_forward_packet(self, packet, destiny):
        self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[0].ip} - packet: {packet.id}")
        destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
        destiny_link.packets_queue.append(packet)
            
    def forward_packet_to_another_gateway(self, packet, destiny):
        if destiny.network_interfaces[1] not in packet.trace:
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[1].ip} - packet: {packet.id}")
            destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
            destiny_link.packets_queue.append(packet)

    def connect_to_another_network(self, network_gateway_address):
        """Connect to another network through a given network gateway e.g router or switch"""
        if network_gateway_address != self.machine.network_interfaces[1].ip:
            # verify if there is a machine in simulation_core with this address using the second network interface
            neighbor_gateway = next(filter(lambda machine: machine.network_interfaces[1].ip == network_gateway_address,  self.simulation_core.all_gateways), None)
            if neighbor_gateway:
                if neighbor_gateway.type == 'router' or neighbor_gateway.type == 'switch':
                    # verify if there is already a connection between the peer and the source
                    if not self.machine.verify_if_connection_link_already_exists(neighbor_gateway):
                        _link = FogWirelessLink(self.simulation_core)
                        _link.network_interface_1 = self.machine.network_interfaces[1]
                        _link.network_interface_2 = neighbor_gateway.network_interfaces[1]
                        neighbor_gateway.peers.append(self)
                        self.machine.peers.append(neighbor_gateway)
                        self.simulation_core.all_links.append(_link)
                        self.machine.links.append(_link)
                        neighbor_gateway.links.append(_link)
                        self.neighbor_gateways.append(neighbor_gateway)
                        neighbor_gateway.app.neighbor_gateways.append(self.machine)
                        _link.draw_connection_arrow()
                    else:
                        log.msg(f"Info :  - | {self.machine.name}-{self.machine.type} - Already connected to {network_gateway_address}")
        
class AccessPointApp(BaseApp):
    def __init__(self):
        self.protocol = 'TCP'
        super(AccessPointApp, self).__init__()
        self.neighbor_gateways = []
        self.name = f'AccessPointApp'
        self.base_gateway = None # can be router or switch
        
        
    def main_loop(self):
        if len(self.in_buffer) > 0:
            for packet in self.in_buffer.copy():
                destiny = self.simulation_core.get_machine_by_ip(packet.destiny_addr)
                # verify if destiny is connected peers list, link in ip routering table
                if destiny and destiny in self.machine.peers:
                    packet.trace.append(self.machine.network_interfaces[0])
                    self.direct_forward_packet(packet, destiny)
                # if are not connected to destiny, send the packet to the base gateway
                else:
                    packet.trace.append(self.machine.network_interfaces[1])
                    self.forward_packet_to_another_gateway(packet, self.base_gateway)

                # if are not connected to destiny
                # or dont found any route to forward packets,
                # or packet was successfully forwarded
                # just drop packets from in_buffer
                self.in_buffer.remove(packet)

    def main(self):
        super().main()
        for gtw_addr in self.machine.connected_gateway_addrs:
            self.connect_to_base_gateway(gtw_addr)
        LoopingCall(self.main_loop).start(0.1)
        
    def direct_forward_packet(self, packet, destiny):
        self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[0].ip} - packet: {packet.id}")
        destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
        destiny_link.packets_queue.append(packet)
            
    def forward_packet_to_another_gateway(self, packet, destiny):
        if destiny.network_interfaces[1] not in packet.trace:
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[1].ip} - packet: {packet.id}")
            destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
            destiny_link.packets_queue.append(packet)

    def connect_to_base_gateway(self, network_gateway_address):
        """Connect to gateway e.g router or switch"""
        if network_gateway_address != self.machine.network_interfaces[1].ip:
            # verify if there is a machine in simulation_core with this address using the second network interface
            neighbor_gateway = next(filter(lambda machine: machine.network_interfaces[1].ip == network_gateway_address,  self.simulation_core.all_gateways), None)
            if neighbor_gateway:
                if neighbor_gateway.type == 'router' or neighbor_gateway.type == 'switch':
                    # verify if there is already a connection between the peer and the source
                    if not self.machine.verify_if_connection_link_already_exists(neighbor_gateway):
                        self.base_gateway = neighbor_gateway
                        _link = FogWirelessLink(self.simulation_core)
                        _link.network_interface_1 = self.machine.network_interfaces[1]
                        _link.network_interface_2 = neighbor_gateway.network_interfaces[1]
                        neighbor_gateway.peers.append(self)
                        self.machine.peers.append(neighbor_gateway)
                        self.simulation_core.all_links.append(_link)
                        self.machine.links.append(_link)
                        neighbor_gateway.links.append(_link)
                        self.neighbor_gateways.append(neighbor_gateway)
                        neighbor_gateway.app.neighbor_gateways.append(self.machine)
                        _link.draw_connection_arrow()
                    else:
                        log.msg(f"Info :  - | {self.machine.name}-{self.machine.type} - Already connected to {network_gateway_address}")
        