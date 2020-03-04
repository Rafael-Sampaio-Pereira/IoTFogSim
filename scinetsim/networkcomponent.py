
from twisted.python import log
from scinetsim.functions import import_and_instantiate_class_from_string

class StandardClientNetworkComponent():

    def __init__(self, visual_component, simulation_core, application, is_wireless):

        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self.application = import_and_instantiate_class_from_string(application)
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core
        self.application.is_wireless = is_wireless
        self.network_settings = "tcp:{}:{}".format(self.application.router_addr,self.application.router_port)

    def doStart(self):
        pass
    
    def doStop(self):
        pass
    
    def buildProtocol(self, addr):
        return self.application
