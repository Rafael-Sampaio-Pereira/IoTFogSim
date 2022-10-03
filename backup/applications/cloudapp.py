from twisted.python import log
import json
from datetime import datetime
from twisted.internet.task import LoopingCall
from applications.applicationcomponent import StandardApplicationComponent
from core.functions import create_csv_database_file


class CloudStorageApp(StandardApplicationComponent):
    # This cloud storage App is based on the simple mqtt subscriber App - Rafael Sampaio
    
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
        self.database = create_csv_database_file(self.simulation_core)

        self.screen_name = "\n\n      CLOUD STORAGE\n"+self.transport.getHost().host+":"+str(self.transport.getHost().port)
        self.simulation_core.updateEventsCounter(self.screen_name+" - Connected to mqtt broker")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        # After connect, send the subscribe request - Rafael Sampaio
        self.subscribe()
        self.update_name_on_screen(self.screen_name)
        self.save_protocol_in_simulation_core(self) 

        self.create_connection_animation()

        # self.save_to_database()
        LoopingCall(self.save_to_database).start(10.0)  

    def subscribe(self):
                
        msg = {
                "action": "subscribe",
                "topic": "any",
                "content": "None"
            }

        self.simulation_core.updateEventsCounter(self.screen_name+" - sending MQTT SUBSCRIBE REQUEST")
        package = self.build_package(msg, 'mqtt')
        self.send(package)

    def dataReceived(self, data):
        self.put_package_in_buffer(data)

    def save_to_database(self):

        try:
            if self.verify_buffer():
                
                for package in self._buffer.copy():
                    destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package) 
                                        
                    payload = json.dumps(payload)
                    
                    if payload.startswith('{'):

                        payload = json.loads(payload)

                        to_file = ""

                        # extract energy content - Rafael Sampaio
                        for obj in payload['content']:
                            data = json.loads(json.dumps(obj['data']))

                            for key, value in data.items():
                                to_file += key+": "+value+","
                            
                            to_file +="stored_at:"+datetime.now().isoformat()

                            print(to_file, file = self.database, flush=True)


                        # Print the received data on the sreen.  - Rafael Sampaio
                        # self.update_alert_message_on_screen(payload['content'])

                        format = "%d/%m/%Y - %H:%M:%S"
                        now = datetime.now()
                        now = now.strftime(format)

                        # Print  on the sreen the last time that received any data.  - Rafael Sampaio
                        self.update_alert_message_on_screen("Last received:"+now)

                        self._buffer.remove(package)
                    
                    else:
                        # Print the received data on the sreen.  - Rafael Sampaio
                        self.update_alert_message_on_screen(payload)

                        self._buffer.remove(package)
                
                self.simulation_core.updateEventsCounter("CLOUD STORAGE - Saving to the database.")


        except Exception as e:
            log.msg(e)
        
        # reactor.callLater(1, self.save_to_database)


    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False 