
import datetime
import random
from twisted.internet.task import LoopingCall
from apps.base_app import BaseApp
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from apps.smart_traits.channel import Channel
from apps.smart_traits.volume import Volume
from core.functions import sleep
import names


DEFAULT_PACKET_LENGTH = 1024

class SmartTvApp(BaseApp):

    def __init__(self):
        super(SmartTvApp, self).__init__()
        self.port = 8975
        self.name ='SmartTv'
        self.protocol = 'UDP'
        self.channel = Channel(5, 'Record')
        self.volume = Volume(7)
        self.source = 'Antena'

    def set_source(self, source=None):
        if self.machine.is_turned_on:
            self.source = source or names.get_last_name()
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} souce: {self.source}")

    def set_volume(self, volume=None):
        if self.machine.is_turned_on:
            self.volume.current_volume = volume or random.uniform(0,50)
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} volume: {self.volume.current_volume}")

    def set_channel(self, channel_code=None, channel_name=None):
        if self.machine.is_turned_on:
            self.channel.channel_code = channel_code or random.randint(1,20)
            self.channel.channel_name = channel_name or names.get_last_name()
            self.simulation_core.updateEventsCounter(f"{self.last_actor} has setted a new {self.machine.name} channel: {self.channel.channel_code} - {self.channel.channel_name}")

    def main(self):
        super().main()
        stream_server_address = '192.168.1.2'
        stream_server_port = 8976
        self.send_packet(
            stream_server_address,
            stream_server_port,
            'Open Session Request',
            DEFAULT_PACKET_LENGTH
        )
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(0.1))
        
    def main_loop(self):
        if self.machine.is_turned_on:
            if len(self.in_buffer) > 0:
                for packet in self.in_buffer.copy():
                    self.simulation_core.updateEventsCounter(f"{self.name}-{self.protocol} - proccessing packet {packet.id}. Payload: {packet.payload}")
                    self.in_buffer.remove(packet)
                    del packet
                    
    def update_dataset(self):
        if not self.dataset_file_has_header:
            dataset_csv_header = 'day; time; machine; status; power consumption (Kw); source; channel; volume; last actor'
            print(dataset_csv_header, file = self.dataset_file, flush=True)
            self.dataset_file_has_header = True
            
        def get_row():
            row = \
            f"{self.simulation_core.clock.elapsed_days};"+\
            f"{str(datetime.timedelta(seconds=self.simulation_core.clock.elapsed_seconds))};"+\
            f"{self.machine.name};"+\
            f"{'ON' if self.machine.is_turned_on else 'OFF'};"+\
            f"{round(self.machine.current_consumption,3) if self.machine.is_turned_on else 0};"+\
            f"{self.source if self.machine.is_turned_on else '-'};"+\
            f"{str(self.channel.channel_code)+' - '+self.channel.channel_name if self.machine.is_turned_on else '-'};"+\
            f"{str(self.volume.current_volume) if self.machine.is_turned_on else '-'};"+\
            f"{self.last_actor}"
            return row
        
        def core(row):
            print(row, file = self.dataset_file, flush=True)
        reactor.callInThread(core, get_row())
