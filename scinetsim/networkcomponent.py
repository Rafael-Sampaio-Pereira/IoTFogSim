from scinetsim.applicationcomponent import StandardServerApplicationComponent
from scinetsim.applicationcomponent import StandardClientApplicationComponent
from twisted.python import log

class StandardServerNetworkComponent():

    def __init__(self, host, port, visual_component, simulation_core):
        self.host = host
        self.port = port
        self.network_settings = "tcp:interface={}:{}".format(str(self.host),self.port)
        self.visual_component = visual_component
        self.simulation_core = simulation_core

    def doStart(self):
        log.msg("Initializing Server...")
    
    def doStop(self):
        log.msg("Shotdown Server...")
    
    def buildProtocol(self, addr):
        return StandardServerApplicationComponent(self.visual_component, self.simulation_core)


class StandardClientNetworkComponent():

    def __init__(self, serverHost, serverPort, visual_component, simulation_core):
        self.serverHost = serverHost
        self.serverPort = serverPort 
        self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)
        self.visual_component = visual_component
        self.simulation_core = simulation_core

    def doStart(self):
        log.msg("Initializing client...")
    
    def doStop(self):
        log.msg("Shotdown client...")
    
    def buildProtocol(self, addr):
       return StandardClientApplicationComponent(self.visual_component, self.simulation_core)