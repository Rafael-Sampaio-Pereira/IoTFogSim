#!/usr/bin/env python3
from twisted.internet import protocol
from twisted.python import log
import uuid
from twisted.internet import reactor
import time
import codecs
import json

#from scinetsim.functions import extract_package_contents

from applications.applicationcomponent import StandardApplicationComponent

protocol.Protocol.noisy = False












# #VERSÃO ANTIGA - INFUNCIONAL

# # The router application code acts as a proxy application. it receives packages and send it out to the destiny addr.
# # Requests are received at the 'RouterIN' interface. Then these requests are send to destiny using the 'RouterOUT' interface.
# # Ween destiny sends response, the reply wiil be received by the 'RouterOUT', that will use 'RouterIN' to send response to the client.
# #  - Rafael Sampaio

# class RouterApp:
    
#     def __init__(self):
#         self.all_connectors_list = []
#         self.visual_component = None
#         self.simulation_core = None

#     def start(self, addr, port):
#         try:
#             factory = RouterINFactory()
#             factory.noisy = False
#             factory.simulation_core = self.simulation_core
#             factory.visual_component = self.visual_component
#             factory.all_connectors_list = self.all_connectors_list
#             reactor.listenTCP(port, factory, interface=addr)

#         except Exception as e:
#             log.msg("Error: %s" % str(e))


# class RouterIN(StandardApplicationComponent):

#     noisy = False
 

#     def __init__(self, factory):
#         self._buffer = []
#         self.client = None
#         self.factory = factory
#         self.visual_component = self.factory.visual_component
#         self.simulation_core = self.factory.simulation_core

#         self.buffer_verification_time = 3

#         self.router_out_factory = RouterOUTFactory()
#         self.router_out_factory.noisy = False
#         self.router_out_factory.all_connectors_list = self.factory.all_connectors_list
#         self.router_out_factory.server = self

#         self.verify_buffer_and_forward_packages()

        

#     def connectionMade(self):
#         self.transport.setTcpKeepAlive(1)
#         self.terminateLater = None

#         self.update_name_on_screen(self.transport.getHost().host+":"+str(self.transport.getHost().port)) 


#     def dataReceived(self, data):
#         #self.simulation_core.updateEventsCounter("Router receiving package")

#         self.put_package_in_buffer(data)

        
#     def verify_buffer_and_forward_packages(self):
#         try:
#             #print(self._buffer)
#             for package in self._buffer:
                
#                 destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
                
#                 if destiny_port != 5000:
#                     # este ptinter server para mostrar q as mesnagens de respostas enviadas pelo broker estão chegando até aqui, logo o problema é daqui pra baixo
#                     print(package)

#                 if(payload):
#                     if payload == ('ARP_REQUEST'):
#                         pass
#                     elif payload == ('DHCP_REQUEST'):
#                         pass
                    
#                     else:

#                         # if this connection already exists use that - Rafael Sampaio
#                         con = self.find_connector_by_destiny_address_and_port(destiny_addr, destiny_port)          
                        
#                         if con:
#                             if con.router_out_protocol.transport.getPeer().port == destiny_port:

#                                 destiny_protocol = con.router_out_protocol
#                                 #print(destiny_protocol)

#                                 # self.destiny_addr = destiny_addr
#                                 # self.destiny_port = destiny_port
#                                 # self.source_addr = source_addr
#                                 # self.source_port = source_port

#                                 destiny_protocol.send(package)
#                                 self._buffer.remove(package)
#                                 self.simulation_core.updateEventsCounter("Router Forwarding package from existing connection")

#                         # else start a new connection- Rafael Sampaio
#                         else:
#                             def save_conection_and_send_fisrt_message(p):
#                                 con = Connector(destiny_addr, destiny_port, p)
#                                 self.factory.all_connectors_list.append(con)
                                
#                                 # After save connection, send the first message - Rafael Sampaio
                                
#                                 # self.destiny_addr = destiny_addr
#                                 # self.destiny_port = destiny_port
#                                 # self.source_addr = source_addr
#                                 # self.source_port = source_port

#                                 con.router_out_protocol.send(package)
#                                 self._buffer.remove(package)
#                                 self.simulation_core.updateEventsCounter("Router Forwarding package from new conection")

#                             from twisted.internet.endpoints import TCP4ClientEndpoint
#                             from twisted.internet.endpoints import connectProtocol

#                             factory = self.router_out_factory

#                             router_out_protocol = RouterOUT(factory)
#                             factory.protocol = router_out_protocol
#                             point = TCP4ClientEndpoint(reactor, destiny_addr, destiny_port)
#                             d = connectProtocol(point, router_out_protocol)
#                             d.addCallback(save_conection_and_send_fisrt_message)


#                 else:
#                     log.msg("It's looks like something is going wrong. Data maybe empty!")
#         except Exception as e:
#             log.msg(e)

#         reactor.callLater(self.buffer_verification_time, self.verify_buffer_and_forward_packages)


#     def find_connector_by_destiny_address_and_port(self, destiny_addr, destiny_port):
#         for connector in self.factory.all_connectors_list:
#             if connector.router_out_protocol.transport.getPeer().host == destiny_addr and connector.router_out_protocol.transport.getPeer().port == destiny_port:
#                 print(connector.router_out_protocol.transport.getHost().port)
#                 print(connector.destiny_port)
#                 print(destiny_port)
#                 return connector





# class RouterOUT(StandardApplicationComponent):

#     noisy = False

#     def connectionMade(self):
#         self.terminateLater = None
#         self.transport.setTcpKeepAlive(1)
#         self.factory.server.transport.setTcpKeepAlive(1)
#         self.factory.noisy = False
        
#         self.factory.server.client = self

#         self.visual_component = self.factory.server.visual_component
#         self.simulation_core = self.factory.server.simulation_core


#     def dataReceived(self, data):
        
#         try:
#             if data.endswith(b"\n"):
#                 packages = data.split(b"\n")
#                 for package in packages:
#                     if package != b'':
#                         #print(package)
#                         #print(self.factory.server._buffer)
#                         self.factory.server._buffer.append(package)
#                         #print(self.factory.server._buffer)

#         except Exception as e:
#             log.msg(e)


#     def __init__(self, factory): #OK
#         self.factory = factory



# class Connector(object):
    
#     def __init__(self, destiny_addr, destiny_port, router_out_protocol):
        
#         self.destiny_addr = destiny_addr
#         self.destiny_port = destiny_port
#         self.router_out_protocol = router_out_protocol

# class RouterOUTFactory(protocol.ClientFactory): #OK
    
#     def __init__(self):
#         self.all_connectors_list = []


# class RouterINFactory(protocol.ServerFactory): #OK
#     protocol = RouterIN

#     def __init__(self):
#         self.all_connectors_list = []
#         self.visual_component = None
#         self.simulation_core = None

#     def buildProtocol(self, addr):
#         return RouterIN(self)