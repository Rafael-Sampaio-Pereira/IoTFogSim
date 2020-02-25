from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver
from twisted.internet.defer import Deferred

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        self.factory.node.activeTransports.append(self.transport)
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        self.factory.node.activeTransports.remove(self.transport)
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage("{} has left the channel.".format(self.name))

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine("Name taken, please choose another!")
            return
        self.sendLine("Welcome, {}".format(name))
        self.broadcastMessage("{} has joined the channel.".format(name))
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "[%s]>> %s" % (self.name, message)
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)

class ChatFactory(Factory):
    """Handle all the nodes' connection"""
    def __init__(self, node):
        self.users = {}
        self.node = node

    def buildProtocol(self, addr):
        return ChatProtocol(self)

class Node:
    def __init__(self, endpoint, clock, stop=None):
        self.Factory = ChatFactory
        self._endpoint = endpoint
        self._listenStarting = None
        self._listeningPort = None
        self.activeTransports = []
        if stop is not None:
            print("Scheduling stop.", stop)
            clock.callLater(stop, self.stop)

    def listen(self):
        self._listenStarting = self._endpoint.listen(self.Factory(self))
        def setPort(port):
            self._listeningPort = port
        def clear(whatever):
            self._listenStarting = None
            return whatever
        self._listenStarting.addCallback(setPort).addBoth(clear)

    def stop(self):
        if self._listenStarting is not None:
            self._listenStarting.cancel()
        if self._listeningPort is not None:
            self._listeningPort.stopListening()
        for transport in self.activeTransports[:]:
            transport.abortConnection()

class Organization:
    def __init__(self, reactor):
        self.reactor = reactor
        self.nodes = []

    def port(self, number):
        return TCP4ServerEndpoint(self.reactor, number)

    def create_leader(self):
        leader_node = Node(self.port(8000), self.reactor, 5)
        leader_node.listen()
        self.nodes.append(leader_node)

    def create_more_nodes(self):
        node_1 = Node(self.port(8001), self.reactor)
        node_2 = Node(self.port(8002), self.reactor)
        self.nodes.append(node_1)
        self.nodes.append(node_2)

    def activate(self):
        self.nodes[1].listen()
        self.nodes[2].listen()

def main(reactor):
    org = Organization(reactor)
    org.create_leader()
    org.create_more_nodes()
    org.activate()
    return Deferred()

if __name__ == '__main__':
    from twisted.internet.task import react
    react(main)