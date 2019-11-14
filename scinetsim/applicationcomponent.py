from twisted.internet import protocol
from twisted.python import log
import tkinter
from config.settings import ICONS_PATH

class StandardClientApplicationComponent(protocol.Protocol):
    
    def __init__(self, visual_component, canvas):
        self.visual_component = visual_component
        self.canvas = canvas

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
        self.send(b"test data")

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
    
    def send(self, message):
        self.transport.write(message)

    def dataReceived(self, data):     
        # Print the received data on the sreen.  - Rafael Sampaio
        self.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received data %s"%(data))


class StandardServerApplicationComponent(protocol.Protocol):
    
    def __init__(self, visual_component, canvas):
        self.visual_component = visual_component
        self.canvas = canvas

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
        self.send(b"test data")

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
    
    def send(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        # Print the received data on the sreen.  - Rafael Sampaio
        self.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received data %s"%(data))