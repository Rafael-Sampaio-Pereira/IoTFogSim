
from twisted.python import log
from scinetsim.functions import import_and_instantiate_class_from_string

class StandardServerNetworkComponent():

    def __init__(self, visual_component, simulation_core, application):

        self.visual_component = visual_component
        self.simulation_core = simulation_core
        #self.application = application

        self.application = import_and_instantiate_class_from_string(application)
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core

        #self.network_settings = "tcp:interface={}:{}".format(str(self.application.source_addr),self.application.source_port)


    def doStart(self):
        log.msg("Initializing Server...")
    
    def doStop(self):
        log.msg("Shotdown Server...")
    
    def buildProtocol(self, addr):

        return self.application


class StandardClientNetworkComponent():

    def __init__(self, visual_component, simulation_core, application):

        print(application)
        self.visual_component = visual_component
        self.simulation_core = simulation_core

        self.application = import_and_instantiate_class_from_string(application)
        self.application.visual_component = self.visual_component
        self.application.simulation_core = self.simulation_core

        self.network_settings = "tcp:{}:{}".format(self.application.router_addr,self.application.router_port)

    def doStart(self):
        log.msg("Initializing client...")
    
    def doStop(self):
        log.msg("Shotdown client...")
    
    def buildProtocol(self, addr):
        

        return self.application


    


# class RouterNetworkComponent():
    
#     def __init__(self, visual_component, simulation_core, application, _buffer):

#         self.visual_component = visual_component
#         self.simulation_core = simulation_core
#         #self.application = application

#         self.application = import_and_instantiate_class_from_string(application)
#         self.application.visual_component = self.visual_component
#         self.application.simulation_core = self.simulation_core
#         self.application._buffer = _buffer

#         #self.network_settings = "tcp:interface={}:{}".format(str(self.application.source_addr),self.application.source_port)


#     def doStart(self):
#         pass
#         # log.msg("Initializing Server...")
    
#     def doStop(self):
#         log.msg("Shotdown Server...")
    
#     def buildProtocol(self, addr):

#         return self.application

