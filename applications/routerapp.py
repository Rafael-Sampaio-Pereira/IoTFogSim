 
from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.endpoints import TCP4ServerEndpoint

protocol.ServerFactory.noisy = False

class RouterApp:
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.router_factory = None

    # def start(self, addr, port):
        
    #     router_factory = RouterFactory(self.visual_component, self.simulation_core)
    #     router_factory.noisy = False
    #     # starting message broker server - Rafael Sampaio
    #     endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(router_factory)
    #     # updating broker name (ip:port) on screen - Rafael Sampaio
    #     self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(addr+":"+str(port)))
    
    def start(self, addr, port):
        self.router_factory = RouterFactory(self.visual_component, self.simulation_core)
        self.router_factory.noisy = False
        self.router_factory.protocol = RouterAppProtocol

        endpoint = TCP4ServerEndpoint(reactor, port)
        listenStarting = endpoint.listen(self.router_factory)

        #reactor.listenTCP(port, factory, interface=addr)
        

        def save_protocol(p):

            # create a simple connection just to start the factory listen_potocol - Rafael_sampaio
            from twisted.internet.endpoints import TCP4ClientEndpoint
            from twisted.internet.protocol import ClientFactory
            endpoint = TCP4ClientEndpoint(reactor, addr, port)
            factory = ClientFactory()
            factory.protocol = protocol.Protocol
            whenConnected = endpoint.connect(factory)

            def cbConnected(connectedProtocol):
                self.router_factory.listen_protocol.visual_component = self.visual_component
                self.router_factory.listen_protocol.simulation_core = self.simulation_core
                self.simulation_core.allProtocols.add(self.router_factory.listen_protocol)

            def ebConnectError(reason):
                print("NAO FOI POSSIVEL CONNECTAR AO ROTEADOR")

            whenConnected.addCallbacks(cbConnected, ebConnectError)



            print(self.router_factory.listen_protocol)
            #self.simulation_core.allProtocols.add(self.router_factory.listen_protocol)

        #factory.addCallbacks(self.save_protocol_in_simulation_core(self))
        listenStarting.addCallback(save_protocol)




class RouterAppProtocol(StandardApplicationComponent):

    def __init__(self):
        self.buffer = None
        self.client = None
        self.visual_component = None
        self.simulation_core =  None
    
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

    def write(self, data):
        self.transport.write(data)

    
       

    def connectionMade(self):
        # updating broker name (ip:port) on screen - Rafael Sampaio
        #self.update_name_on_screen(addr+":"+str(port))
        self.save_protocol_in_simulation_core(self)
      
        

 
class RouterFactory(protocol.Factory):

    protocol = RouterAppProtocol

    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.listen_protocol = None

    # def buildProtocol(self, addr):
        # self.listen_protocol = RouterAppProtocol(self)
        # return self.listen_protocol


    def buildProtocol(self, address):
        proto = protocol.ServerFactory.buildProtocol(self, address)
        self.listen_protocol = proto
        return proto


 
class ClientProtocol(StandardApplicationComponent):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        #self.create_connection_animation()

    def dataReceived(self, data):
        self.factory.server.write(data)
 
    def write(self, data):
        if data:
            self.transport.write(data)
 
    
 
