
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp

DEFAULT_MIPS = 1024

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
