
from twisted.python import log
from core.functions import import_and_instantiate_class_from_string

class StandardClientNetworkComponent():

    def __init__(self, application):
        
        self.application = application
        self.network_settings = "tcp:{}:{}".format(self.application.gateway_addr, self.application.gateway_port)

    def doStart(self):
        pass
    
    def doStop(self):
        pass
    
    def buildProtocol(self, addr):
        return self.application
