from twisted.internet import protocol
from twisted.python import log
import json
import codecs
from twisted.internet import reactor, protocol, endpoints
from applications.applicationcomponent import StandardApplicationComponent


class DatabaseServerApp:
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        
        server_factory = DatabaseServerAppFactory(self.visual_component, self.simulation_core)
        server_factory.noisy = False
        # starting Database server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(server_factory)
        # updating server name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(addr+":"+str(port))) 

class DatabaseServerAppFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core

    def buildProtocol(self, addr):
        return DatabaseServerAppProtocol(self)

class DatabaseServerAppProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.visual_component = factory.visual_component
        self.simulation_core = factory.simulation_core
        self.factory = factory
        self.router_addr = "127.0.0.1"
        self.router_port = 8081

        #self.network_settings = "tcp:interface={}:{}".format(str(self.router_addr),self.router_port)

    def connectionMade(self):
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.simulation_core.updateEventsCounter("Connection received")
        # self.create_connection_animation()
        self.save_protocol_in_simulation_core(self)     

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection failed")
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection lost")

    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data)
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from client %s"%(payload))

        package = {
                        "destiny_addr": source_addr,
                        "destiny_port": source_port,
                        "source_addr": self.source_addr,
                        "source_port": self.source_port,
                        "type": 'http',
                        "payload": "ack"
                    }
        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        self.send(msg_bytes)

        self.simulation_core.updateEventsCounter("Sending ACK")
        