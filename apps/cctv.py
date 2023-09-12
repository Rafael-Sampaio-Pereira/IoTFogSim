
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp


DEFAULT_PACKET_LENGTH = 1024

# CCTV = CLOSE-CIRCUIT TELEVISION = CFTV(Brazil)

class CCTVClientApp(BaseApp):

    def __init__(self):
        super(CCTVClientApp, self).__init__()
        self.port = 8975
        self.name ='CCTV Client'
        self.protocol = 'UDP'
        self.cctv_server_address = '172.148.0.2'
        self.cctv_server_port = 8000
        
        
    def main(self):
        super().main()
        self.send_packet(
            self.cctv_server_address,
            self.cctv_server_port,
            'Connect to Camera Request',
            DEFAULT_PACKET_LENGTH
        )
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(0.7))
        
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                    self.in_buffer.remove(packet)
                    del packet
                    

class CameraApp(BaseApp):

    def __init__(self):
        super(CameraApp, self).__init__()
        self.port = 8000
        self.name ='CCTV Camera'
        self.protocol = 'UDP'
        self.cctv_server_address = '172.148.0.2'
        self.cctv_server_port = 8000
        self.data_frame_counter = 0
        
        
    def main(self):
        super().main()
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(0.7))
        
    def send_stream_data_frame(self, destiny_addr, destiny_port, length):
        self.data_frame_counter += 1
        data = f'STREAM DATA FRAME {self.data_frame_counter}'
        self.send_packet(
            destiny_addr,
            destiny_port,
            data,
            length
        )
        
    def main_loop(self):
        if self.machine.is_turned_on:
            self.send_stream_data_frame(self.cctv_server_address, self.cctv_server_port, DEFAULT_PACKET_LENGTH)
                    
                
                
class CCTVServerApp(BaseApp):
    def __init__(self):
        super(CCTVServerApp, self).__init__()
        self.port = 8000
        self.name ='CCTV Server'
        self.data_frame_counter = 0
        self.protocol = 'UDP'
        self.connected_clients = []

    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    if packet.destiny_port == self.port:
                        if packet.payload == 'Connect to Camera Request':
                            self.connected_clients.append(
                                {
                                    "addr": packet.source_addr,
                                    "port": packet.source_port
                                }
                            )
                        
                        else:
                            self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                            
                            if len(self.connected_clients) >0:
                                for client in self.connected_clients.copy():
                                    self.send_packet(client['addr'],  client['port'], packet.payload, packet.length)
                            
                        self.in_buffer.remove(packet)
                        del packet
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
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(0.7))
