from applications.applicationcomponent1 import StandardServerApplicationComponent
from applications.applicationcomponent1 import StandardClientApplicationComponent
from twisted.python import log

class StandardServerNetworkComponent():

    def __init__(self, host, port, visual_component, canvas):
        self.host = host
        self.port = port
        #self.network_settings = "tcp:interface={}:{}".format(str(self.host),self.port)
        self.visual_component = visual_component
        self.canvas = canvas

    def onPacktReceive(self):
        pass

    def onStart(self):
        log.msg("Initializing Server...")
    
    def onStop(self):
        log.msg("Shotdown Server...")

    def connect(self):
        pass


class StandardClientNetworkComponent():

    def __init__(self, serverHost, serverPort, visual_component, canvas):
        self.serverHost = serverHost
        self.serverPort = serverPort 
        #self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)
        self.visual_component = visual_component
        self.canvas = canvas

    def onPacktReceive(self):
        pass

    def onStart(self):
        log.msg("Initializing client...")
    
    def onStop(self):
        log.msg("Shotdown client...")

    def connect(self):
        pass