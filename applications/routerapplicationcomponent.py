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


# The router application code acts as a proxy application. it receives packages and send it out to the destiny addr.
# Requests are received at the 'RouterIN' interface. Then these requests are send to destiny using the 'RouterOUT' interface.
# Ween destiny sends response, the reply wiil be received by the 'RouterOUT', that will use 'RouterIN' to send response to the client.
#  - Rafael Sampaio

class RouterApplication:
    
    def __init__(self):
        self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None

    def start(self, addr, port):
        try:
            factory = RouterINFactory()
            factory.simulation_core = self.simulation_core
            factory.visual_component = self.visual_component
            factory.all_connectors_list = self.all_connectors_list
            reactor.listenTCP(port, factory, interface=addr)

        except Exception as e:
            log.msg("Error: %s" % str(e))


class RouterIN(StandardApplicationComponent):

    noisy = False
 

    def __init__(self, factory):
        self.buffer = None
        self.client = None
        self.factory = factory
        self.visual_component = self.factory.visual_component
        self.simulation_core = self.factory.simulation_core

    def connectionMade(self):
        self.transport.setTcpKeepAlive(1)
        self.terminateLater = None

    def write(self, data):
        self.transport.write(data)

    def connectionLost(self, reason):
        log.msg("Connection was closed %s" % (reason.getErrorMessage()))

    def dataReceived(self, data):
        self.simulation_core.updateEventsCounter("Router receiving package")
        try:
            destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data)
            
            if(payload):
                if payload == ('ARP_REQUEST'):
                    pass
                elif payload == ('DHCP_REQUEST'):
                    pass
                
                else:

                    factory = RouterOUTFactory()
                    factory.noisy = False
                    factory.all_connectors_list = self.factory.all_connectors_list
                    factory.server = self

                    # if this connection already exists use that - Rafael Sampaio
                    con = self.find_connector_by_source_and_destiny_addresses(destiny_addr, source_addr)

                    if con:
                        con.router_out_protocol.transport.write(data)
                        self.simulation_core.updateEventsCounter("Router Forwarding package")

                    # else start a new connection- Rafael Sampaio
                    else:
                        def save_conection_and_send_fisrt_message(p):
                            con = Connector(destiny_addr, source_addr, self, p)
                            self.factory.all_connectors_list.append(con)
                            
                            # After save connection, send the first message - Rafael Sampaio
                            con = self.find_connector_by_source_and_destiny_addresses(destiny_addr, source_addr)
                            con.router_out_protocol.transport.write(data)
                            self.simulation_core.updateEventsCounter("Router Forwarding package")

                        from twisted.internet.endpoints import TCP4ClientEndpoint
                        from twisted.internet.endpoints import connectProtocol

                        router_out_protocol = RouterOUT(factory)
                        factory.protocol = router_out_protocol
                        point = TCP4ClientEndpoint(reactor, destiny_addr, destiny_port)
                        d = connectProtocol(point, router_out_protocol)
                        d.addCallback(save_conection_and_send_fisrt_message)


            else:
                log.msg("It's looks like something is going wrong. Data maybe empty!")
        except Exception as e:
            log.msg(e)


    def find_connector_by_source_and_destiny_addresses(self, destiny_addr, source_addr):
        for con in self.factory.all_connectors_list:
            if con.destiny_addr == destiny_addr and con.source_addr == source_addr:
                return con
            else:
                return False


class RouterOUT(StandardApplicationComponent):

    noisy = False

    def connectionMade(self):
        self.terminateLater = None
        self.transport.setTcpKeepAlive(1)
        self.factory.server.transport.setTcpKeepAlive(1)
        self.factory.noisy = False
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''


    def dataReceived(self, data):
        if(data):
            connector = self.find_connector_by_router_out_protocol()

            self.factory.server.write(data)

        else:
            log.msg("It's looks like something is going wrong. Data maybe empyt!")

    def write(self, data): #OK
        if data:
            self.transport.write(data)

    def connectionLost(self, reason): #OK
        log.msg("Connection was closed: %s" % (reason.getErrorMessage()))

    def __init__(self, factory): #OK
        self.factory = factory

    def find_connector_by_router_out_protocol(self): #OK
        for con in self.factory.all_connectors_list:
            if con.router_out_protocol == self:
                return con


class Connector(object):
    
    def __init__(self, destiny_addr, source_addr, router_in_protocol, router_out_protocol):
        
        self.source_addr = source_addr
        self.destiny_addr = destiny_addr
        self.router_out_protocol = router_out_protocol
        self.router_in_protocol = router_in_protocol


class RouterOUTFactory(protocol.ClientFactory): #OK
    
    def __init__(self):
        self.all_connectors_list = []


class RouterINFactory(protocol.ServerFactory): #OK
    protocol = RouterIN

    def __init__(self):
        self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None

    def buildProtocol(self, addr):
        return RouterIN(self)