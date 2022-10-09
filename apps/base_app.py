import uuid
from components.packets import Packet
from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet import reactor



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
        reactor.callFromThread(self.main)

    def send_packet(self, destiny_addr, destiny_port, payload, length):
        _packet = Packet(
            self.simulation_core,
            self.machine.network_interfaces[0].ip,
            self.port,
            destiny_addr,
            destiny_port,
            payload,
            length
        )
        _packet.trace.append(self.machine.network_interfaces[0])
        self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.network_interfaces[0].ip}) creating packet {_packet.id} with {length}")
        if len(self.machine.links) > 0:
            if self.machine.network_interfaces[0].is_wireless:
                self.machine.propagate_signal()
            self.machine.links[0].packets_queue.append(_packet)
            peer = None
            if self.machine.network_interfaces[0] != self.machine.links[0].network_interface_1:
                peer=self.machine.links[0].network_interface_1
            else:
                peer=self.machine.links[0].network_interface_2
            self.simulation_core.updateEventsCounter(f"{self.machine.network_interfaces[0].ip} \u27FC   \u2344 \u27F6  {peer.ip} - packet: {_packet.id}")
        else:
            log.msg(f"Info :  - | {self.machine.type}({self.machine.network_interfaces[0].ip}) are not connected to a peer. Packet {_packet.id} can not be sent")
