
from twisted.internet import protocol, reactor,endpoints
from twisted.python import log
    

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
        pass

    def run(self):
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
        pass

    def run(self):
        client = endpoints.clientFromString(reactor, "tcp:127.0.0.1:5000")
        client.connect(mqttPublisher())

# ========== SUBSCRIBER ==========


