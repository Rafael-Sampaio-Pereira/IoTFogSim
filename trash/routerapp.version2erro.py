#!/usr/bin/env python3
from twisted.internet import protocol
from twisted.internet import protocol, reactor, endpoints
from twisted.python import log
import uuid
from twisted.internet import reactor
import time
import codecs
import json

from scinetsim.networkcomponent import RouterNetworkComponent

from applications.applicationcomponent import StandardApplicationComponent

protocol.Protocol.noisy = False



class RouterApp:
    
    def __init__(self):
        #self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None

    def start(self, addr, port):
        try:
            factory = RouterFactory()
            factory.noisy = False
            factory.simulation_core = self.simulation_core
            factory.visual_component = self.visual_component
            # factory.all_connectors_list = self.all_connectors_list
            reactor.listenTCP(port, factory, interface=addr)

        except Exception as e:
            log.msg("Error: %s" % str(e))


class RouterFactory(protocol.ServerFactory):
    #protocol = RouterApp

    def __init__(self):
        # self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None

    def buildProtocol(self, addr):
        return RouterInProtocol(self)


class RouterInProtocol(StandardApplicationComponent):

    def __init__(self, factory):
        self._buffer = []
        self.factory = factory
        self.visual_component = self.factory.visual_component
        self.simulation_core = self.factory.simulation_core

        self.network_component = RouterNetworkComponent(self.visual_component, self.simulation_core, "applications.routerapp.RouterOutProtocol", self._buffer)

        self.buffer_verification_time = 3
        self.verify_buffer_and_forward_packages()


    def dataReceived(self, data):
        self.put_package_in_buffer(data)


    def verify_buffer_and_forward_packages(self):
        try:
            #print(self._buffer)
            for package in self._buffer:
                
                destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(package)
                
                if destiny_port != 5000:
                    # este ptinter server para mostrar q as mesnagens de respostas enviadas pelo broker estão chegando até aqui, logo o problema é daqui pra baixo
                    print(package)

                if(payload):
                    if payload == ('ARP_REQUEST'):
                        pass
                    elif payload == ('DHCP_REQUEST'):
                        pass
                    
                    else:

                        def save_conection_and_send__message(p):
                        
                            p.send(package)
                            self._buffer.remove(package)
                            

                        from twisted.internet.endpoints import TCP4ClientEndpoint
                        from twisted.internet.endpoints import connectProtocol

                        #factory = self.router_out_factory

                        # ptl = protocol.ClientFactory()
                        # factory.protocol = router_out_protocol
                        # point = TCP4ClientEndpoint(reactor, destiny_addr, destiny_port)
                        # d = connectProtocol(point, self)
                        # d.addCallback(save_conection_and_send__message)


                        client = endpoints.clientFromString(reactor, "tcp:{}:{}".format(destiny_addr,destiny_port))
                        client.connect(self.network_component)
                        


                else:
                    log.msg("It's looks like something is going wrong. Data maybe empty!")
        except Exception as e:
            log.msg(e)

        reactor.callLater(self.buffer_verification_time, self.verify_buffer_and_forward_packages)



class RouterOutProtocol(StandardApplicationComponent):

    def __init__(self):
        #self.all_connectors_list = []
        self.visual_component = None
        self.simulation_core = None
        self._buffer = None
    
    def dataReceived(self, data):
        self.put_package_in_buffer(data)

    def connectionMade(self):
        pass
