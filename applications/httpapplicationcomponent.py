from twisted.internet import protocol
from twisted.python import log
import json
import codecs

from scinetsim.functions import extract_package_contents


class HttpClientApplicationComponent(protocol.Protocol):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 5000 

        self.router_addr = "127.0.0.1"
        self.router_port = 8081


        self.network_settings = "tcp:{}:{}".format(self.router_addr,self.router_port)

    def connectionMade(self):
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port

        package = {
                        "destiny_addr": self.destiny_addr,
                        "destiny_port": self.destiny_port,
                        "source_addr": self.source_addr,
                        "source_port": self.source_port,
                        "type": 'http',
                        "payload": "test data"
                    }
        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        self.send(msg_bytes)
        

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("Connection failed")
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection lost")
    
    def send(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = extract_package_contents(data) 
        # Print the received data on the sreen.  - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received from server %s"%(payload))


class HttpServerApplicationComponent(protocol.Protocol):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core = None

        self.source_addr = "127.0.0.1"
        self.source_port = 5000 

        self.destiny_addr = None
        self.destiny_port = None

        self.router_addr = "127.0.0.1"
        self.router_port = 80

        self.network_settings = "tcp:interface={}:{}".format(str(self.router_addr),self.router_port)

    def connectionMade(self):
        pass
        #self.send(b"test data")
        

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection failed")
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection lost")
    
    def send(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = extract_package_contents(data)
        # Print the received data on the sreen.  - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received from client %s"%(payload))

        package = {
                        "destiny_addr": self.destiny_addr,
                        "destiny_port": self.destiny_port,
                        "source_addr": self.source_addr,
                        "source_port": self.source_port,
                        "type": 'http',
                        "payload": "reply test data"
                    }
        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        self.send(msg_bytes)
        