from twisted.internet import protocol
from twisted.python import log

class SubscriberApplication(protocol.Protocol):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None

        self.serverHost = serverHost
        self.serverPort = serverPort
        self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)

    def connectionMade(self):
        self.simulation_core.updateEventsCounter("Connected to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
        self.send(b"test data")
        

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("Connection failed")
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("connection lost")
    
    def send(self, message):
        self.transport.write(message)
        self.simulation_core.updateEventsCounter("Sending data to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))

    def dataReceived(self, data):     
        # Print the received data on the sreen.  - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received data %s"%(data))
        self.simulation_core.updateEventsCounter("Received data from %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))