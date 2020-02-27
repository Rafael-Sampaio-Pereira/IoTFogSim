from twisted.internet import protocol
from twisted.python import log
import json
import codecs
from scinetsim.standarddevice import Connection


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
        package = package
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

    def update_name_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(msg))

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("Connection failed")
    
    def connectionLost(self, reason):
        try:
            if self.simulation_core:
                log.msg('connection lost:', reason.getErrorMessage())
                self.simulation_core.updateEventsCounter("connection lost")
                self.simulation_core.allProtocols.remove(self)
        except NameError:
            log.msg("The requested simulation_core is no longer available")

    def send(self, message):
        self.transport.write(message+b"\n")

    def put_package_in_buffer(self, data):
        if data.endswith(b"\n"):
            packages = data.split(b"\n")
            for package in packages:
                if package != b'':
                    self._buffer.append(package)

    
    def save_protocol_in_simulation_core(self, proto):
        try:
            if self.simulation_core:
                if self.simulation_core:
                    self.simulation_core.allProtocols.add(proto)
                    #print(self.simulation_core.allProtocols)
            else:
                print("This divice have no simulation core instance")
        except NameError:
            log.msg("The requested simulation_core is no longer available")
        

    def create_connection_animation(self):
        # this method can only be called on the connectionMade method of the clients devices. do not use that in servers instances - Rafael Sampaio
        con = Connection(self.simulation_core, self, self.transport.getPeer().host, self.transport.getPeer().port)
        self.simulation_core.allConnections.add(con)
        


        # if len(self.simulation_core.allConnections) > 0:
        #     for connection in self.simulation_core.allConnections.copy():
                    
    
        #         d1 = connection.device1.transport.getHost()
        #         d2 = connection.device1.transport.getHost()
        #         _self = self.transport.getHost()
        #         peer = self.transport.getPeer()

        #         if ((d1.host == _self.host and d1.port == _self.port) and (d2.host == peer.host and d1.port == peer.port)) or ((d2.host == _self.host and d2.port == _self.port) and (d1.host == peer.host and d1.port == peer.port)):

        #             # if the conection animation arrow already exist, just pass - Rafael Sampaio
        #             pass
        #         else:
        #             con = Connection(self.simulation_core, self, self.transport.getPeer().host, self.transport.getPeer().port)
        #             self.simulation_core.allConnections.add(con)
        # else:
        #     con = Connection(self.simulation_core, self, self.transport.getPeer().host, self.transport.getPeer().port)
        #     self.simulation_core.allConnections.add(con)

