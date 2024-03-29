from twisted.python import log
from twisted.internet.task import LoopingCall
from core.engine.network import extract_ip_prefix
from apps.base_app import BaseApp
from twisted.internet import reactor


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
        if self.machine.is_turned_on:
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
                                reactor.callFromThread(self.forward_packet_to_another_gateway, packet, route_hops[0])
                        else:
                            log.msg(f"Info :  - | {self.machine.type}({self.machine.network_interfaces[1].ip}) could not find a route to {destiny_addr_prefix} subnetwork")
                    
                    # if are not connected to destiny
                    # or dont found any route to forward packets,
                    # or packet was successfully forwarded
                    # just drop packets from in_buffer
                    self.in_buffer.remove(packet)
                        
    def main(self):
        super().main()
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(0.1))
        
    def direct_forward_packet(self, packet, destiny):
        self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[0].ip} - packet: {packet.id}")
        destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
        destiny_link.packets_queue.append(packet)
            
    def forward_packet_to_another_gateway(self, packet, destiny):
        if destiny.network_interfaces[1] not in packet.trace:
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[1].ip} \u27FC   \u2344 \u27F6  {destiny.network_interfaces[1].ip} - packet: {packet.id}")
            destiny_link = self.machine.verify_if_connection_link_already_exists(destiny)
            if destiny_link:
                destiny_link.packets_queue.append(packet)
