from twisted.internet import protocol
from twisted.python import log
import json
import codecs
from twisted.internet import reactor, protocol, endpoints
from applications.applicationcomponent import StandardApplicationComponent


class HttpClientApp(StandardApplicationComponent):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.source_addr = None
        self.source_port = None

        self.destiny_addr = "127.0.0.1"
        self.destiny_port = 8080 

        self.gateway_addr = "127.0.0.1"
        self.gateway_port = 8081


        self.network_settings = "tcp:{}:{}".format(self.gateway_addr,self.gateway_port)

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connected to http server")
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.create_connection_animation()
        self.simulation_core.updateEventsCounter("sending HTTP REQUEST")

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
        destiny_addr, destiny_port, source_addr, source_port, _type, payload = self.extract_package_contents(data) 
        # Print the received data on the sreen.  - Rafael Sampaio
        self.update_alert_message_on_screen(payload)
        log.msg("Received from server %s"%(payload))
        self.simulation_core.updateEventsCounter("Http response received")






class HttpServerApp:
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        
        server_factory = HttpServerAppFactory(self.visual_component, self.simulation_core)
        server_factory.noisy = False
        # starting http server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(server_factory)
        # updating server name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(addr+":"+str(port))) 

class HttpServerAppFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core

    def buildProtocol(self, addr):
        return HttpServerAppProtocol(self)

class HttpServerAppProtocol(StandardApplicationComponent):
    
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
                        "payload": "HTTP 1.0 / GET response"
                    }
        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        self.send(msg_bytes)

        self.simulation_core.updateEventsCounter("Sending HTTP RESPONSE")


# class HTTPServerNewApp(StandardApplicationComponent):
    
class HTTPServerNewApp:
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

    def start(self, addr, port):
        broker_factory = BrokerFactory(self.visual_component, self.simulation_core)
        broker_factory.noisy = False
        # starting message broker server - Rafael Sampaio
        endpoints.serverFromString(reactor, "tcp:interface={}:{}".format(addr, port)).listen(broker_factory)
        # updating broker name (ip:port) on screen - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text="\n\n\nHTTP SERVER\n"+str(addr+":"+str(port))) 


class BrokerProtocol(StandardApplicationComponent):
    
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.visual_component = self.factory.visual_component
        self.simulation_core =  self.factory.simulation_core
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.destiny_addr = self.transport.getPeer().host
        self.destiny_port = self.transport.getPeer().port

        self.transport.setTcpKeepAlive(1)
        self.terminateLater = None
        # self.create_connection_animation()


        response_package = self.build_package("MQTT_ACK")
        self.send(response_package)
        self.save_protocol_in_simulation_core(self)
        

        # # if the factory aint have a protocol for external connections, this wiil be it - Rafael Sampaio
        # # the official protocol is able to forward packets from the factory shared buffer to cloud - Rafael Sampaio
        if not self.factory.official_protocol:
            self.factory.official_protocol = self
            self.create_connection_animation()
            




    def send(self, message):

        self.transport.write(message+b"\n")


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
                        "payload": "HTTP 1.0 / GET response"
                    }
        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        self.send(msg_bytes)

        self.simulation_core.updateEventsCounter("Sending HTTP RESPONSE")
       


class BrokerFactory(protocol.Factory):
    def __init__(self, visual_component, simulation_core):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.total_received_bytes = 0

        self.incoming_buffer = set()

        # this protocol will be used for send data to the cloud - Rafael Sampaio
        # it will be the first protocol open by a client connection. - Rafael Sampaio
        # after client connects if this still None the current client connection will be the officcial protocol - Rafael Sampaio
        self.official_protocol = None


    def buildProtocol(self, addr):
        return BrokerProtocol(self)





