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


    def extract_package_contents(self, package):
        try:
            package = package.decode("utf-8")
            package = str(package)[0:]
            json_msg = json.loads(package)

            return json_msg["destiny_addr"], json_msg["destiny_port"], json_msg["source_addr"], json_msg["source_port"], json_msg["type"], json_msg["payload"]
        
        except Exception as e:
            log.msg(e)

    def update_alert_message_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text=str(msg))

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("Connection failed")
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection lost")

    def send(self, message):
        self.transport.write(message)
