 
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
 
# Adapted from http://stackoverflow.com/a/15645169/221061
class RouterApp(StandardApplicationComponent):
    def __init__(self):
        self.buffer = None
        self.client = None
 
    def connectionMade(self):
        pass
 
    # Client =&amp;amp;gt; Proxy
    def dataReceived(self, data):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data)
 
        reactor.connectTCP(destiny_addr, destiny_port, factory)

        if self.client:
            self.client.write(data)
        else:
            self.buffer = data
 
    # Proxy =&amp;amp;gt; Client
    def write(self, data):
        self.transport.write(data)

    def start(self, addr, port):
        factory = protocol.ServerFactory()
        factory.protocol = RouterApp
    
        reactor.listenTCP(port, factory, interface=addr)

 
class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
 
    # Server =&amp;amp;gt; Proxy
    def dataReceived(self, data):
        self.factory.server.write(data)
 
    # Proxy =&amp;amp;gt; Server
    def write(self, data):
        if data:
            self.transport.write(data)
 
    
 
