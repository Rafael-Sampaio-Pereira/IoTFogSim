
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep


DEFAULT_PACKET_LENGTH = 1024

class StreamClientApp(BaseApp):

    def __init__(self):
        super(StreamClientApp, self).__init__()
        self.port = 8975
        self.name ='StreamClient'
        self.protocol = 'UDP'
        
        
    def main(self):
        super().main()
        self.send_packet(
            '192.168.1.2',
            8976,
            'Open Session Request',
            DEFAULT_PACKET_LENGTH
        )
        LoopingCall(self.main_loop).start(0.1)
        
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                    self.in_buffer.remove(packet)
                    
                
                
class StreamServerApp(BaseApp):
    def __init__(self):
        super(StreamServerApp, self).__init__()
        self.port = 8976
        self.name ='Stream Server'
        self.has_started_streaming = False
        self.stream_client_address = None
        self.stream_client_port = None
        self.data_frame_counter = 0

    @inlineCallbacks
    def main_loop(self):
        if self.machine.is_turned_on:
            if self.has_started_streaming:
                self.send_stream_data_frame(self.stream_client_address, self.stream_client_port, DEFAULT_PACKET_LENGTH)
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if packet.destiny_port == self.port:
                        self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                        self.in_buffer.remove(packet)
                        if not self.has_started_streaming:
                            self.has_started_streaming = True
                            self.stream_client_address = packet.source_addr
                            self.stream_client_port = packet.source_port
                            yield sleep(3)
                            
                    else:
                        self.in_buffer.remove(packet)
                        self.send_http_404_response(packet.source_addr, packet.source_port, DEFAULT_PACKET_LENGTH)       
        
    def send_stream_data_frame(self, destiny_addr, destiny_port, length):
        self.data_frame_counter += 1
        data = f'STREAM DATA FRAME {self.data_frame_counter}'
        self.send_packet(
            destiny_addr,
            destiny_port,
            data,
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
        LoopingCall(self.main_loop).start(0.7)
