 
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import connectProtocol

protocol.ServerFactory.noisy = False

class RouterApp:
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.router_factory = None

    def start(self, addr, port):

        # updating name on screen - Rafael Sampaio
        self.screen_name  = addr+":"+str(port)
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(self.screen_name))

        # get start to listen to connections(i.e. inputs) - Rafael Sampaio
        self.router_factory = RouterFactory(self.visual_component, self.simulation_core)
        self.router_factory.noisy = False
        self.router_factory.protocol = RouterAppProtocol

        # starting the router as server to wait for input connections connections - Rafael Sampaio
        endpoint = TCP4ServerEndpoint(reactor, port, interface=addr)
        listenStarting = endpoint.listen(self.router_factory)

        def save_protocol(p):

            # create a simple connection just to start the factory listen_potocol - Rafael_sampaio
            endpoint = TCP4ClientEndpoint(reactor, addr, port)
            factory = ClientFactory()
            factory.noisy = False
            factory.protocol = protocol.Protocol
            whenConnected = endpoint.connect(factory)

            def cbConnected(connectedProtocol):
                self.router_factory.listen_protocol.visual_component = self.visual_component
                self.router_factory.listen_protocol.simulation_core = self.simulation_core
                self.simulation_core.allProtocols.add(self.router_factory.listen_protocol)

            def ebConnectError(reason):
                print("Error while try to connect to the router")

            whenConnected.addCallbacks(cbConnected, ebConnectError)

        listenStarting.addCallback(save_protocol)


class RouterAppProtocol(StandardApplicationComponent):

    def __init__(self):
        self.buffer = None
        self.client = None
        self.visual_component = None
        self.simulation_core =  None
    
    def dataReceived(self, package):
        # Extracting package contents - Rafael Sampaio
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)

        def save_protocol(proto):
            try:
                if self.simulation_core:
                    # saving the protocol used by the router as out(i.e. endponit to connect to a destiny host and redirect package) - Rafael Sampaio         
                    self.simulation_core.allProtocols.add(proto)
                    proto.create_connection_animation()
            except NameError:
                log.msg("The requested simulation_core is no longer available")

        # get start to connect redirect the receivede package - Rafael Sampaio
        factory = protocol.ClientFactory()
        factory.noisy = False
        cur_protocol = ClientProtocol()
        cur_protocol.visual_component = self.visual_component
        cur_protocol.simulation_core = self.simulation_core
        factory.protocol = cur_protocol
        cur_protocol.factory = factory
        factory.server = self
        
        # conncecting to destiny and routering received packages - Rafael Sampaio
        point = TCP4ClientEndpoint(reactor, destiny_addr, destiny_port)
        d = connectProtocol(point, cur_protocol)
        # After connect, save the protocol - Rafael Sampaio
        d.addCallback(save_protocol)

        if self.client:
            self.client.write(package)
        else:
            self.buffer = package

    def write(self, package):
        self.transport.write(package)

    def connectionMade(self):
        # saving the router protocol that acts as input(i.e. this receives packages) - Rafael Sampaio
        self.save_protocol_in_simulation_core(self)
      
        
 
class RouterFactory(protocol.Factory):

    protocol = RouterAppProtocol

    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.listen_protocol = None

    def buildProtocol(self, address):
        proto = protocol.ServerFactory.buildProtocol(self, address)
        self.listen_protocol = proto
        return proto

 
class ClientProtocol(StandardApplicationComponent):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        
    def dataReceived(self, data):
        self.factory.server.write(data)
 
    def write(self, data):
        if data:
            self.transport.write(data)
 
    
 
