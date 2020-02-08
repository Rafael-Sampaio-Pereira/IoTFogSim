
from twisted.python import log
from scinetsim.functions import import_and_instantiate_class_from_string

class StandardServerNetworkComponent():

    def __init__(self, host, port, visual_component, simulation_core, application):
        self.host = host
        self.port = port
        self.network_settings = "tcp:interface={}:{}".format(str(self.host),self.port)
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.application = application

    def doStart(self):
        log.msg("Initializing Server...")
    
    def doStop(self):
        log.msg("Shotdown Server...")
    
    def buildProtocol(self, addr):
        application = import_and_instantiate_class_from_string(self.application)
        application.visual_component = self.visual_component
        application.simulation_core = self.simulation_core

        return application


class StandardClientNetworkComponent():

    def __init__(self, serverHost, serverPort, visual_component, simulation_core, application):
        self.serverHost = serverHost
        self.serverPort = serverPort 
        self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.application = application

    def doStart(self):
        log.msg("Initializing client...")
    
    def doStop(self):
        log.msg("Shotdown client...")
    
    def buildProtocol(self, addr):
        application = import_and_instantiate_class_from_string(self.application)
        application.visual_component = self.visual_component
        application.simulation_core = self.simulation_core

        return application

