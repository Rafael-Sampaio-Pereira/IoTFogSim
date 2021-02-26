
from twisted.internet import protocol, reactor
from twisted.python import log
import json
import uuid
import sys
from datetime import datetime
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet.task import LoopingCall
from applications.applicationcomponent import StandardApplicationComponent

from scinetsim.functions import create_csv_database_file

from libs import lzw
from libs import delta_encode as de

# 600 == 10 min / 900 == 15 min
read_interval = 600

class FogDataReducitonBrokerApp:

    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        
        broker_factory = BrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text="\n\n\nAGREGADOR\n"+str(addr+":"+str(port))) 

class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.factory = factory
        self.database = False
        self.incoming_buffer = set()
        

    def connectionLost(self, reason):        
        try:
            if self in factory.subscribers:
                self.factory.subscribers.remove(self)
        except NameError:
            pass
    
    def connectionMade(self):
        self.visual_component = self.factory.visual_component
        self.simulation_core =  self.factory.simulation_core
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.destiny_addr = self.transport.getPeer().host
        self.destiny_port = self.transport.getPeer().port
        response_package = self.build_package("MQTT_ACK")
        self.send(response_package)
        self.save_protocol_in_simulation_core(self)

        LoopingCall(self.forward_packages).start(5.0) 
        
        

    def dataReceived(self, package):

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
        # Print the received data on the sreen.  - Rafael Sampaio

        action, topic_title, content = extract_mqtt_contents(payload)

        if action == "subscribe":
            # Saving the connected protocol to the factory subscribers protocols list set - Rafael Sampaio
            self.factory.subscribers.add(self)
            self.send_mqtt_acknowledgement(source_addr, source_port)

        elif action == "publish":
            # send ack to the sender of the received package - Rafael Sampaio
            self.send_mqtt_acknowledgement(source_addr, source_port)
            if content:
                for measue_values in content:
                    self.incoming_buffer.add(json.dumps(measue_values))
            # self.send_package_to_all_subscribers(package)
            self.update_last_package_received_time_on_screen()

    def send_package_to_all_subscribers(self, package):
        
        for subscriber in self.factory.subscribers:
            self.source_addr = subscriber.transport.getHost().host
            self.source_port = subscriber.transport.getHost().port
            self.destiny_addr = subscriber.transport.getPeer().host
            self.destiny_port = subscriber.transport.getPeer().port
            subscriber.send(package)

    def send_mqtt_acknowledgement(self, destiny_addr, destiny_port):
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        response_package = self.build_package("MQTT_ACK"+str(uuid.uuid4().fields[-1]))
        self.send(response_package)


    def update_last_package_received_time_on_screen(self):
        format = "%d/%m/%Y - %H:%M:%S"
        now = datetime.now()
        now = now.strftime(format)

        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now+"\n")

    def send(self, message):
        self.transport.write(message+b"\n")


    def aggregate_all_packages_from_buffer(self):
        if len(self.incoming_buffer) > 0:
            aggregated_data = '{ "aggregated_data": ['
            self.temp_buffer = self.incoming_buffer.copy()
            # aggregating each data in buffer for each subscribed- Rafael Sampaio
            for _package in self.temp_buffer:
                
                aggregated_data = aggregated_data + _package + ','

                # remove the original package from buffer - Rafael Sampaio
                self.incoming_buffer.remove(_package)
            
            # removing last comma - Rafael Sampaio
            aggregated_data = aggregated_data[:-1]
            aggregated_data = aggregated_data+']}'

            return aggregated_data


    def lzw_aggregated_data_compression(self, aggregated_data):
        compressed_data = lzw.compress(aggregated_data)
        # transforming packge in bytes to send it via TCP - Rafael Sampaio
        compressed_data = bytes(str(compressed_data), encoding='utf8')
        return compressed_data


    def delta_encoding_and_lzw_aggregated_data_compression(self, aggregated_data):
        compressed_data = lzw.compress(aggregated_data)
        compressed_data = de.delta_encoder(compressed_data)

        # transforming packge in bytes to send it via TCP - Rafael Sampaio
        compressed_data = bytes(str(compressed_data), encoding='utf8')
        return compressed_data

    def forward_packages(self):
        aggregated_data = self.aggregate_all_packages_from_buffer()
        if aggregated_data:
            # compressed_data = self.lzw_aggregated_data_compression(aggregated_data)
            compressed_data = self.delta_encoding_and_lzw_aggregated_data_compression(aggregated_data)
            if compressed_data:
                self.send_package_to_all_subscribers(compressed_data)
        
        



                
        


    

class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers = set()
        self.total_received_bytes = 0

    def buildProtocol(self, addr):
        return BrokerProtocol(self)


def extract_mqtt_contents(package):
    try:
        package = json.dumps(package)
        package = str(package)[0:]
        json_msg = json.loads(package)
        return json_msg["action"], json_msg["topic"], json_msg["content"]
    except Exception as e:
        log.msg(e)

MQTT_ACK = {"action": "response", "topic": "sensor_metering", "content": "MQTT_ACK"}





# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||



class SCADAResearchApp(StandardApplicationComponent):
    # This SCADA App is based on the simple mqtt subscriber App - Rafael Sampaio
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.screen_name = None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5100 

        self.gateway_addr = "127.0.0.1"
        self.gateway_port = 8081

        

        self._buffer = []

        self.network_settings = "tcp:{}:{}".format(self.gateway_addr,self.gateway_port)

    def connectionMade(self):
        # creating and opening a csv database file - Rafael Sampaio
        self.database = create_csv_database_file(self.simulation_core, description='CLOUD')

        self.screen_name = "\n\n      SCADA\n"+self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the subscribe request - Rafael Sampaio
        self.subscribe()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 

        self.create_connection_animation()

        # self.save_to_database()
        LoopingCall(self.save_to_database).start(32.0)  

    def subscribe(self):
                
        msg = {
                "action": "subscribe",
                "topic": "sensor_metering",
                "content": "None"
            }

        self.simulation_core.updateEventsCounter(self.screen_name+" - sending MQTT SUBSCRIBE REQUEST")
        package = self.build_package(msg)
        self.send(package)

    def dataReceived(self, data):

        self.put_package_in_buffer(data)

        format = "%d/%m/%Y - %H:%M:%S"
        now = datetime.now()
        now = now.strftime(format)
        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now)


    def extract_energy_content(self, payload):
        pass


    def lzw_aggregated_data_decompression(self, compressed_aggregated_data):
        if compressed_aggregated_data.startswith('['):
            # converting the received dictionary from str list to int list -Rafael Sampaio
            compressed_aggregated_data = compressed_aggregated_data[1:-1]
            compressed_aggregated_data = list(map(int, compressed_aggregated_data.split(',')))
            decompressed_data = lzw.decompress(compressed_aggregated_data)
            return str(decompressed_data)

    def delta_encoding_and_lzw_aggregated_data_decompression(self, compressed_aggregated_data):
        if compressed_aggregated_data.startswith('['):
            # converting the received dictionary from str list to int list -Rafael Sampaio
            compressed_aggregated_data = compressed_aggregated_data[1:-1]
            compressed_aggregated_data = list(map(int, compressed_aggregated_data.split(',')))
            decompressed_data = de.delta_decoder(compressed_aggregated_data)
            decompressed_data = lzw.decompress(decompressed_data)
            return str(decompressed_data)

    def save_to_database(self):

        try:
            if self.verify_buffer():
                for package in self._buffer.copy():
                    
                    pack = package.decode("utf-8")
                    pack = str(pack)[0:]

                    # pack = self.lzw_aggregated_data_decompression(pack)
                    pack = self.delta_encoding_and_lzw_aggregated_data_decompression(pack)

                    if pack:
                        
                        pack = json.loads(pack)
                        to_file = ""

                        # extract energy content - Rafael Sampaio
                        for obj in pack["aggregated_data"]:
                            print('AQUI 2')
                            data = json.loads(json.dumps(obj['data']))
                            to_file = obj['id']+","+obj['source']+","+data['voltage']+","+data['current']+","+data['frequency']+","+data['active_power']+","+data['aparent_power']+","+data['power_factor']+","+ obj['created_at']+","+"stored_at:"+datetime.now().isoformat()
                            
                            print(to_file, file = self.database, flush=True)

                    self._buffer.remove(package)
                
                self.simulation_core.updateEventsCounter("SCADA - Saving to the database.")


        except Exception as e:
            log.msg(e)


    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False 

