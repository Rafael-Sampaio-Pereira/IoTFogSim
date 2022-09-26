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
        self.protocol = 'TCP' # can be UDP or TCP
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
            self.machine.ip,
            self.port,
            destiny_addr,
            destiny_port,
            payload,
            MIPS
        )
        _packet.trace.append(self)
        self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.ip}) creating packet {_packet.id}")
        if len(self.machine.links) > 0:
            self.machine.links[0].packets_queue.append(_packet)
            self.simulation_core.updateEventsCounter(f"{self.machine.type}({self.machine.ip}) sending packet {_packet.id} to {destiny_addr}")
        else:
            log.msg(f"Info : - | {self.machine.type}({self.machine.ip}) are not connected to a peer. Packet {_packet.id} can not be sent")

class SimpleWebClientApp(BaseApp):

    def __init__(self):
        super(SimpleWebClientApp, self).__init__()
        self.port = 80
        self.name ='WEBClient'
    
    def main(self):
        super().main()
        self.machine.connect_to_peer('192.168.1.1')
        self.send_packet(
            '192.168.1.10',
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
        self.machine.connect_to_peer('192.168.1.1')
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Start listen on port {self.port}")
        LoopingCall(self.main_loop).start(0.1)

class RouterApp(BaseApp):
    def __init__(self):
        super(RouterApp, self).__init__()
        self.protocol = 'TCP'
        # NEEDS TO IMPLEMENTS ROTERING PROTOCOL

class RouterWithAccessPointApp(RouterApp):
    def __init__(self):
        super(RouterWithAccessPointApp, self).__init__() 