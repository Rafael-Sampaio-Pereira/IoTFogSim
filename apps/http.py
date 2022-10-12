
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp
from twisted.internet import reactor


DEFAULT_PACKET_LENGTH = 1024

class SimpleWebClientApp(BaseApp):

    def __init__(self):
        super(SimpleWebClientApp, self).__init__()
        self.port = 80
        self.name ='WEBClient'
        
        
    def main(self):
        super().main()
        self.send_packet(
            '192.168.1.2',
            80,
            'HTTP 1.0 POST request',
            DEFAULT_PACKET_LENGTH
        )
        LoopingCall(self.main_loop).start(0.1)
        
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                    self.in_buffer.remove(packet)
                    
                    
class ContinuosRequetWebClientApp(BaseApp):

    def __init__(self):
        super(ContinuosRequetWebClientApp, self).__init__()
        self.port = 80
        self.name ='WEBClient'
        # self.servers_address = ['192.168.0.2', '192.168.1.2', '172.148.0.2']
        self.servers_address = ['192.168.0.2']
        
    def main(self):
        super().main()
        LoopingCall(self.check_in_buffer).start(0.3)
        LoopingCall(self.main_loop).start(10)
        
    def main_loop(self):
        cont=0
        if self.machine.is_turned_on:
            for server_addr in self.servers_address:
                cont+=1
                reactor.callLater(cont*10.0, self.send_packet, server_addr, 80, 'HTTP 1.0 POST request', DEFAULT_PACKET_LENGTH)
                
class SimpleWebServerApp(BaseApp):
    def __init__(self):
        super(SimpleWebServerApp, self).__init__()
        self.port = 80
        self.name ='WEBServer'

    
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if packet.destiny_port == self.port:
                        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                        self.in_buffer.remove(packet)
                        self.send_http_200_response(packet.source_addr, packet.source_port, 'HTTP 1.0 response', DEFAULT_PACKET_LENGTH)
                    else:
                        self.in_buffer.remove(packet)
                        self.send_http_404_response(packet.source_addr, packet.source_port, DEFAULT_PACKET_LENGTH)
                        
        
    def send_http_200_response(self, destiny_addr, destiny_port, response, length):
        self.send_packet(
            destiny_addr,
            destiny_port,
            response,
            length
        )
        
    def send_http_404_response(self, destiny_addr, destiny_port, length):
        self.send_packet(
            destiny_addr,
            destiny_port,
            'HTTP 1.0 404 - NOT FOUND',
            length
        )

    def main(self):
        super().main()
        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - Start listen on port {self.port}")
        LoopingCall(self.main_loop).start(0.07)
