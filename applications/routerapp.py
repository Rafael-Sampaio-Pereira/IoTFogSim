 
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent

protocol.ServerFactory.noisy = False
 
class RouterApp(StandardApplicationComponent):

    # protocol.ServerFactory.noisy = False
    # protocol.Protocol.noisy = False

    def __init__(self):
        self.buffer = None
        self.client = None
        self.visual_component = None
        self.simulation_core =  None
 
    def connectionMade(self):
        pass
 
    # Client =&amp;amp;gt; Proxy
    def dataReceived(self, data):
        factory = protocol.ClientFactory()
        factory.noisy = False
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
        factory.noisy = False
        factory.protocol = RouterApp
        reactor.listenTCP(port, factory, interface=addr)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.update_name_on_screen(addr+":"+str(port)) 

 
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
 
    
 
