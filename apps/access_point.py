from twisted.python import log
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp


class AccessPointApp(BaseApp):
    def __init__(self):
        self.protocol = 'TCP'
        super(AccessPointApp, self).__init__()
        self.neighbor_gateways = []
        self.name = f'AccessPointApp'
        self.base_gateway = None # can be router or switch
        
        
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    destiny = self.simulation_core.get_machine_by_ip(packet.destiny_addr)
                    # verify if destiny is connected peers list, link in ip routering table
                    if destiny and destiny in self.machine.peers:
                        if self.machine.network_interfaces[0].is_wireless:
                            self.machine.propagate_signal()
                        packet.trace.append(self.machine.network_interfaces[0])
                        self.direct_forward_packet(packet, destiny)
                    # if are not connected to destiny, send the packet to the base gateway
                    else:
                        if self.machine.network_interfaces[1].is_wireless:
                            self.machine.propagate_signal()
                        packet.trace.append(self.machine.network_interfaces[1])
                        self.forward_packet_to_another_gateway(packet, self.base_gateway)

                    # if are not connected to destiny
                    # or dont found any route to forward packets,
                    # or packet was successfully forwarded
                    # just drop packets from in_buffer
                    self.in_buffer.remove(packet)

    def main(self):
        super().main()
        if len(self.neighbor_gateways ) > 0:
            # first gateway in connected list will be the base gateway
            itf = self.simulation_core.get_network_interface_by_ip(self.neighbor_gateways[0].network_interfaces[1].ip)
            if itf:
                self.base_gateway = itf.machine
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

