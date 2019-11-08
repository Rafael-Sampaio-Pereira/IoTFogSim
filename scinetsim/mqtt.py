
from twisted.internet import protocol, reactor,endpoints
from twisted.python import log
from utils.draggableImage import DraggableImage
import tkinter
    

# ========== BROKER ==========

class mqttBrokerProtocol(protocol.Protocol):
    def __int__(self):
        pass

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
    
    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
    
    def write(self, message):
        self.transport.write(message)

class mqttBroker():
    def doStart(self):
        log.msg("Initializing mqtt broker...")
    
    def doStop(self):
        log.msg("Shotdown mqtt broker...")
    
    def buildProtocol(self, addr):
        return mqttBrokerProtocol()
    
    def __init__(self):
        self.canvas = None
        self.icon = None

    def setCanvas(self, canvas):
        self.canvas = canvas

    def run(self):
        self.icon = DraggableImage(self.canvas, "graphics/icons/scinetsim_restfull_server.png", 100, 100)
        endpoints.serverFromString(reactor, "tcp:interface=127.0.0.1:5000").listen(mqttBroker())

# ========== PUBLISHER ==========

class mqttPublisherProtocol(protocol.Protocol):
    def __int__(self):
        pass

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
    
    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())

    def write(self, message):
        self.transport.write(message)
    

class mqttPublisher():
    def doStart(self):
        log.msg("Initializing mqtt publisher...")
    
    def doStop(self):
        log.msg("Shotdown mqtt publisher...")
    
    def buildProtocol(self, addr):
        return mqttPublisherProtocol()

    def __init__(self):
        self.protocol = mqttPublisherProtocol()
        self.canvas = None
        self.icon = None
        self.message_label = tkinter.Label(self.canvas, text="", width=40)

    def setCanvas(self, canvas):
        self.canvas = canvas

    def run(self):
        self.icon = DraggableImage(self.canvas, "graphics/icons/scinetsim_arduino_uno.png", 200, 100)
        client = endpoints.clientFromString(reactor, "tcp:127.0.0.1:5000")
        client.connect(mqttPublisher())
        self.message_label.pack(side="top", fill="x")
        self.show_message_on_label()


    def show_message_on_label(self):
        self.message_label.configure(text="textonatela")

# ========== SUBSCRIBER ==========


