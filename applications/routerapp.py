# #!/usr/local/bin/python
# # $Id$
# # $Source$
# import getopt
# import string
# import sys

# from twisted.internet import protocol
# from twisted.internet import reactor

# class RouterApp:
    
#     def __init__(self):
#         self.visual_component = None
#         self.simulation_core =  None

#     def start(self, addr, port):
#         reactor.listenTCP(port, DebugHttpServerFactory("127.0.0.1", int(5100)))


# class DebugHttpClientProtocol(protocol.Protocol):
#   """ Client protocol. Writes out the request to the target HTTP server."""
#   """ Response is written to stdout on receipt, and back to the server's"""
#   """ transport when the client connection is lost.                     """

#   def __init__(self, serverTransport):
#         self.serverTransport = serverTransport

#   def sendMessage(self, data):
#     self.transport.write(data)
  
#   def dataReceived(self, data):
#     self.data = data
#     self.transport.loseConnection()

#   def connectionLost(self, reason):
#     #self.serverTransport.write(self.data)
#     self.serverTransport.loseConnection()


# class DebugHttpServerProtocol(protocol.Protocol):
#   """ Server Protocol. Handles data received from client application.   """
#   """ Writes the data to console, then creates a proxy client component """
#   """ and sends the data through, then terminates the client and server """
#   """ connections.                                                      """

#   def dataReceived(self, data):
#     self.data = data

#     client = protocol.ClientCreator(reactor, DebugHttpClientProtocol, self.transport)
#     d = client.connectTCP(self.factory.targetHost, self.factory.targetPort)
#     d.addCallback(self.forwardToClient, client)

#   def forwardToClient(self, client, data):
#     client.sendMessage(self.data)


# class DebugHttpServerFactory(protocol.ServerFactory):
#   """ Server Factory. A holder for the protocol and for user-supplied args """

#   protocol = DebugHttpServerProtocol

#   def __init__(self, targetHost, targetPort):
#     self.targetHost = targetHost
#     self.targetPort = targetPort





from twisted.internet import protocol, reactor
from applications.applicationcomponent import StandardApplicationComponent
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import connectProtocol



class RouterApp:

    
    protocol.ClientFactory.noisy = False
    TCP4ClientEndpoint.noisy = False
    
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
        endpoint.noisy = False
        listenStarting = endpoint.listen(self.router_factory)

        def save_protocol(p):

            # create a simple connection just to start the factory listen_potocol - Rafael_sampaio
            endpoint = TCP4ClientEndpoint(reactor, addr, port)
            endpoint.noisy = False
            factory = ClientFactory()
            factory.noisy = False
            factory.protocol = protocol.Protocol
            whenConnected = endpoint.connect(factory)

            def cbConnected(connectedProtocol):
                self.router_factory.listen_protocol.visual_component = self.router_factory.visual_component
                self.router_factory.listen_protocol.simulation_core = self.router_factory.simulation_core
                self.simulation_core.allProtocols.add(self.router_factory.listen_protocol)

            def ebConnectError(reason):
                print("Error while try to connect to the router")

            whenConnected.addCallbacks(cbConnected, ebConnectError)

        listenStarting.addCallback(save_protocol)


class RouterAppProtocol(StandardApplicationComponent):

    protocol.ClientFactory.noisy = False
    TCP4ClientEndpoint.noisy = False

    def __init__(self):
        self.buffer = None
        self.client = None
        self.visual_component = None
        self.simulation_core =  None
    
    def dataReceived(self, package):

        #print("OPACOTE É %s"%(package))

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
        cur_protocol.noisy = False
        cur_protocol.visual_component = self.visual_component
        cur_protocol.simulation_core = self.simulation_core
        factory.protocol = cur_protocol
        cur_protocol.factory = factory
        factory.server = self
        
        # conncecting to destiny and routering received packages - Rafael Sampaio
        point = TCP4ClientEndpoint(reactor, destiny_addr, destiny_port)
        point.noisy = False
        d = connectProtocol(point, cur_protocol)
        # After connect, save the protocol - Rafael Sampaio
        d.addCallback(save_protocol)

        if self.client:
            self.client.write(package)
            self.client.transport.loseConnection()
        else:
            self.buffer = package

    def write(self, package):
        self.transport.write(package)
        

    def connectionMade(self):
        # saving the router protocol that acts as input(i.e. this receives packages) - Rafael Sampaio
        self.save_protocol_in_simulation_core(self)
      
        
 
class RouterFactory(protocol.Factory):

    protocol.ServerFactory.noisy = False
    protocol = RouterAppProtocol
    noisy = False
    

    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.listen_protocol = None

    def buildProtocol(self, address):
        proto = protocol.ServerFactory.buildProtocol(self, address)
        self.listen_protocol = proto
        return proto

 
class ClientProtocol(StandardApplicationComponent):
    
    def __init__(self):
        self.simulation_core = None

    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
        
    def dataReceived(self, data):
        self.factory.server.write(data)
        
    def connectionLost(self, reason):
        pass     
         
    def write(self, data):
        if data:
            self.transport.write(data)
            
 

 
