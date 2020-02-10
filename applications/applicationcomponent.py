from twisted.internet import protocol
from twisted.python import log
import json
import codecs

class StandardApplicationComponent(protocol.Protocol):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.network_settings = None



    def build_package(self, payload):
    
        package = {
                    "destiny_addr": self.destiny_addr,
                    "destiny_port": self.destiny_port,
                    "source_addr": self.source_addr,
                    "source_port": self.source_port,
                    "type": 'http',
                    "payload": payload
        }

        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        return msg_bytes


    def extract_package_contents(self, msg):
        
        try:
            msg = msg.decode("utf-8")
            msg = str(msg)[0:]
            json_msg = json.loads(msg)

            return json_msg["destiny_addr"], json_msg["destiny_port"], json_msg["source_addr"], json_msg["source_port"], json_msg["type"], json_msg["payload"]
        
        except Exception as e:
            log.msg(e)