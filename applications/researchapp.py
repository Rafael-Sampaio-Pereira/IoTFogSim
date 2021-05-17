
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
from timeit import default_timer as timer
from datetime import timedelta
from datetime import datetime, date
import os
import random
import time
import schedule

# 300.0 == 5 min / 600.0 == 10 min / 900.0 == 15 min
simulation_duaration = 3660.0

#==================================||

read_interval = 900.0
# read_interval = 600.0

algorithm = "proposta"
#algorithm = "baseline"

#==================================||


class FogDataReducitonBrokerApp:

    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def schedule_experiment_simulation_end(self):
        self.simulation_core.updateEventsCounter("Closing simulation: Experiment time has ended. the simulator will be close soon.")
        reactor.stop()

    def start(self, addr, port):
        broker_factory = BrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text="\n\n\nAGGREGATOR\n"+str(addr+":"+str(port))) 

        # scheduling the time to simulation end - Rafael Sampaio
        reactor.callLater(simulation_duaration, self.schedule_experiment_simulation_end)

class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.factory = factory
        self.database = False

        # self.incoming_buffer = set()
        

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

        # if the factory aint have a protocol for external connections, this wiil be it - Rafael Sampaio
        # the official protocol is able to forward packets from the factory shared buffer to cloud - Rafael Sampaio
        if not self.factory.official_protocol:
            self.factory.official_protocol = self
            LoopingCall(self.forward_packages).start(read_interval)

        # LoopingCall(self.forward_packages).start(read_interval)

        # scheduler = schedule.Scheduler()
        # schedule.every(5).minutes.do(self.forward_packages)
        # scheduler.run_pending()
        
        
        

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
                    self.factory.incoming_buffer.add(json.dumps(measue_values))
                    #self.incoming_buffer.add(json.dumps(measue_values))
            
            self.update_last_package_received_time_on_screen()

    def send_package_to_all_subscribers(self, package):
        # saving the send time for experiments file - Rafael Sampaio
        print(datetime.now().isoformat(), file = self.factory.send_time_file, flush=True)        
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

        # Print  on the sreen the last time that received any data. - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now+"\n")

    def send(self, message):
        self.transport.write(message+b"\n")


    def aggregate_all_packages_from_buffer(self):
        if len(self.factory.incoming_buffer) > 0:
            self.simulation_core.updateEventsCounter("AGGREGATOR - Aggregating data.")
            aggregated_data = '{ "aggregated_data": ['
            self.temp_buffer = self.factory.incoming_buffer.copy()
            # aggregating each data in buffer for each subscribed- Rafael Sampaio
            for _package in self.temp_buffer:
                
                aggregated_data = aggregated_data + _package + ','

                # remove the original package from buffer - Rafael Sampaio
                self.factory.incoming_buffer.remove(_package)
            
            # removing last comma - Rafael Sampaio
            aggregated_data = aggregated_data[:-1]
            aggregated_data = aggregated_data+']}'

            return aggregated_data


    def lzw_aggregated_data_compression(self, aggregated_data):
        self.simulation_core.updateEventsCounter("AGGREGATOR - Comppressing data.")
        start_time = timer()
        compressed_data = lzw.compress(aggregated_data)
        # transforming packge in bytes to send it via TCP - Rafael Sampaio
        compressed_data = bytes(str(compressed_data), encoding='utf8')
        end_time = timer()
        elapsed_time = timedelta(seconds=end_time-start_time)
        size = get_real_data_size_in_kilobytes(compressed_data)

        print(elapsed_time, file = self.factory.elapsed_time_file, flush=True)
        print(size, file = self.factory.compressed_size_file, flush=True)
        return compressed_data


    def delta_encoding_and_lzw_aggregated_data_compression(self, aggregated_data):
        self.simulation_core.updateEventsCounter("AGGREGATOR - Comppressing data.")
        start_time = timer()
        compressed_data = lzw.compress(aggregated_data)
        compressed_data = de.delta_encoder(compressed_data)

        # transforming packge in bytes to send it via TCP - Rafael Sampaio
        compressed_data = bytes(str(compressed_data), encoding='utf8')
        end_time = timer()
        elapsed_time = timedelta(seconds=end_time-start_time)
        size = get_real_data_size_in_kilobytes(compressed_data)

        print(elapsed_time, file = self.factory.elapsed_time_file, flush=True)
        print(size, file = self.factory.compressed_size_file, flush=True)
        
        return compressed_data

    def forward_packages(self):
        aggregated_data = self.aggregate_all_packages_from_buffer()
       
        if aggregated_data:
            # saving the received on fog for the database berofe compress and send - Rafael Sampaio
            self.save_to_database(aggregated_data)
            
            # compressing the aggregate data - Rafael Sampaio
            if algorithm == "baseline":
                compressed_data = self.lzw_aggregated_data_compression(aggregated_data)
            elif algorithm == "proposta":
                compressed_data = self.delta_encoding_and_lzw_aggregated_data_compression(aggregated_data)

            if compressed_data:
                self.send_package_to_all_subscribers(compressed_data)



    def save_to_database(self, aggregated_data):
        pack = json.loads(aggregated_data)
        to_file = ""

        # extract energy content - Rafael Sampaio
        for obj in pack["aggregated_data"]:
            data = json.loads(json.dumps(obj['data']))
            to_file = obj['id']+","+obj['source']+","+data['voltage']+","+data['current']+","+data['frequency']+","+data['active_power']+","+data['aparent_power']+","+data['power_factor']+","+ obj['created_at']+","+"stored_at:"+datetime.now().isoformat()
            
            print(to_file, file = self.factory.database, flush=True)
        
        self.simulation_core.updateEventsCounter("AGGREGATOR - Saving to the database.")
        


class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.subscribers = set()
        self.total_received_bytes = 0

        self.incoming_buffer = set()

        # this protocol will be used for send data to the cloud - Rafael Sampaio
        # it will be the first protocol open by a client connection. - Rafael Sampaio
        # after client connects if this still None the current client connection will be the officcial protocol - Rafael Sampaio
        self.official_protocol = None

        # creating and opening a csv files for experiments - Rafael Sampaio
        self.elapsed_time_file = create_csv_file_for_experiments(self.simulation_core, description="compression_time", subdirectory="compression")
        self.send_time_file = create_csv_file_for_experiments(self.simulation_core, description="send_time", subdirectory="transmission")
        self.compressed_size_file = create_csv_file_for_experiments(self.simulation_core, description="compressed_size", subdirectory="payload_size")
        # creating and opening a csv database file - Rafael Sampaio
        self.database = create_csv_database_file(self.simulation_core, description='FOG_UNCOMPRESSED_DATA')

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
        self.database = create_csv_database_file(self.simulation_core, description='CLOUD_DECOMPRESSED_DATA')

        
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

        self.elapsed_time_file = create_csv_file_for_experiments(self.simulation_core, description="decompression_time", subdirectory="compression")
        self.receive_time_file = create_csv_file_for_experiments(self.simulation_core, description="receive_time", subdirectory="transmission")
        self.decompressed_size_file = create_csv_file_for_experiments(self.simulation_core, description="decompressed_size", subdirectory="payload_size")

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
        # prevent the SCADA to save packages such as "mqtt ack" to the buffer, due it dont has any measure compressed value - Rafael Sampaio 
        if not data.startswith(b'{"destin'):
            # simulating latency - Rafael Sampaio
            simulate_5g_latency_for_smart_grids()
            # saving the received time to the csv file - Rafael Sampaio
            print(datetime.now().isoformat()+","+str(data)[0:10]+" ... "+str(data)[-10:], file = self.receive_time_file, flush=True)  

            # self.put_package_in_buffer(data)
            self._buffer.append(data)

        now = datetime.now()
        format = "%d/%m/%Y - %H:%M:%S"
        now = now.strftime(format)
        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
        self.update_alert_message_on_screen("Last received:"+now)


    def extract_energy_content(self, payload):
        pass


    def lzw_aggregated_data_decompression(self, compressed_aggregated_data):
        if compressed_aggregated_data.startswith('['):
            self.simulation_core.updateEventsCounter("SCADA - Decomppressing data.")
            start_time = timer()
            # converting the received dictionary from str list to int list -Rafael Sampaio
            compressed_aggregated_data = compressed_aggregated_data[1:-1]
            compressed_aggregated_data = list(map(int, compressed_aggregated_data.split(',')))
            decompressed_data = lzw.decompress(compressed_aggregated_data)
            end_time = timer()
            elapsed_time = timedelta(seconds=end_time-start_time)
            print(elapsed_time, file = self.elapsed_time_file, flush=True)

            size = get_real_data_size_in_kilobytes(decompressed_data)
            print(size, file = self.decompressed_size_file, flush=True)

            return str(decompressed_data)

    def delta_encoding_and_lzw_aggregated_data_decompression(self, compressed_aggregated_data):
        if compressed_aggregated_data.startswith('['):
            self.simulation_core.updateEventsCounter("SCADA - Decomppressing data.")
            start_time = timer()
            # converting the received dictionary from str list to int list -Rafael Sampaio
            compressed_aggregated_data = compressed_aggregated_data[1:-1]
            compressed_aggregated_data = list(map(int, compressed_aggregated_data.split(',')))
            decompressed_data = de.delta_decoder(compressed_aggregated_data)
            decompressed_data = lzw.decompress(decompressed_data)
            end_time = timer()
            elapsed_time = timedelta(seconds=end_time-start_time)
            print(elapsed_time, file = self.elapsed_time_file, flush=True)

            size = get_real_data_size_in_kilobytes(decompressed_data)
            print(size, file = self.decompressed_size_file, flush=True)

            return str(decompressed_data)

    def save_to_database(self):

        try:
            # verifyng if buffer has package - Rafael Sampaio
            if self.verify_buffer():

                # making a copy of the buffer to iterate over it - Rafael Sampaio
                temp_buffer =self._buffer.copy()

                # creating a auxiliar variable for use to restore a splipted package in the buffer - Rafael Sampaio                
                aux = None

                # Variable the indicates if the package was fully restored(i.e. the package end was found) - Rafael Sampaio
                end_found = False

                # it will store temporarily the values of imcoplete pakages while the algoritm try to sum package - Rafael Sampaio
                backup_buffer = []

                for package in temp_buffer:

                    if package.startswith(b'[') and (package.endswith(b']')):
                        print('AQUI 0')
                        
                        # removing 'b' and converting the packege from bytes to string - Rafael Sampaio
                        pack = package.decode("utf-8")
                        pack = str(pack)[0:]

                        if algorithm == "baseline":
                            pack = self.lzw_aggregated_data_decompression(pack)
                        elif algorithm == "proposta":
                            pack = self.delta_encoding_and_lzw_aggregated_data_decompression(pack)

                        # extracting package contents and saving it to database file - Rafael Sampaio
                        if pack:
                            pack = json.loads(pack)
                            to_file = ""

                            # extract energy content - Rafael Sampaio
                            for obj in pack["aggregated_data"]:
                                data = json.loads(json.dumps(obj['data']))
                                to_file = obj['id']+","+obj['source']+","+data['voltage']+","+data['current']+","+data['frequency']+","+data['active_power']+","+data['aparent_power']+","+data['power_factor']+","+ obj['created_at']+","+"stored_at:"+datetime.now().isoformat()
                                
                                print(to_file, file = self.database, flush=True)

                        # removing the saved package from buffer - Rafael Sampaio
                        self._buffer.remove(package)

                    elif end_found == False:
                        if package.startswith(b'[') and not package.endswith(b']\n') and aux==None:
                            aux = package
                            backup_buffer.append(package)

                        elif not package.startswith(b'[') and not package.endswith(b']\n') and aux != None:
                            aux = aux+package
                            backup_buffer.append(package)

                        elif  package.endswith(b']\n') and aux != None:
                            end_found = True
                            backup_buffer.append(package)
                            aux = aux+package

                            # removing 'b' and converting the packege from bytes to string - Rafael Sampaio
                            pack = aux.decode("utf-8")
                            pack = str(pack)[0:]

                            # removing \n that is the package and indicator in our simulator - Rafael Sampaio
                            pack = pack.rstrip('\n')

                            if algorithm == "baseline":
                                pack = self.lzw_aggregated_data_decompression(pack)
                            elif algorithm == "proposta":
                                pack = self.delta_encoding_and_lzw_aggregated_data_decompression(pack)

                            # extracting package contents and saving it to database file - Rafael Sampaio
                            if pack:
                                
                                pack = json.loads(pack)
                                to_file = ""

                                # extract energy content - Rafael Sampaio
                                for obj in pack["aggregated_data"]:
                                    data = json.loads(json.dumps(obj['data']))
                                    to_file = obj['id']+","+obj['source']+","+data['voltage']+","+data['current']+","+data['frequency']+","+data['active_power']+","+data['aparent_power']+","+data['power_factor']+","+ obj['created_at']+","+"stored_at:"+datetime.now().isoformat()
                                    
                                    print(to_file, file = self.database, flush=True)

                            # removing the parts used to restore packages from buffer - Rafael Sampaio
                            if len(backup_buffer) > 0:
                                for pack in backup_buffer:
                                    self._buffer.remove(pack)
                
                
                self.simulation_core.updateEventsCounter("SCADA - Saving to the database.")


        except Exception as e:
            log.msg(e)


    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False 



def create_csv_file_for_experiments(simulation_core, description="", subdirectory=""):
    file_path = "projects/"+simulation_core.project_name+"/"
    # create experiments directoy if it not exist - Rafael Sampaio
    if subdirectory:
        os.makedirs(file_path+"/experiments/"+subdirectory+"/", exist_ok=True)
    else:
        os.makedirs(file_path+"/experiments/", exist_ok=True)
    temp = "_{:%Y_%m_%d__%H_%M_%S}".format(datetime.now())
    if subdirectory:
        file = file_path+"/experiments/"+subdirectory+"/"+description+temp+".csv"
    else:
        file = file_path+"/experiments/"+description+temp+".csv"
    csv_file = open(file, 'a')
 
    return csv_file


def get_real_data_size_in_kilobytes(data):
    return str(round(len(str(data).encode('utf-8'))/1024,2))+"Kb"



def simulate_5g_latency_for_smart_grids():
    # the paper "A Survey on Low Latency Towards 5G: RAN, Core Network and Caching Solutions"(Parvaez, 2017) shows that
    # latency requirements for smart grids under 5g networks is between 1 and 20ms - Rafael Sampaio
    
    suitable_latency_values = []
    for i in range(1000):
        x = random.gammavariate(0.001, 0.02)
        x = round(x,2)     

        suitable_latency_values.append(x)
    
    latency = random.choice(suitable_latency_values)
    time.sleep(latency)
