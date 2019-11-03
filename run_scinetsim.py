from twisted.internet import reactor
from scinetsim.mqtt import mqttBroker
from scinetsim.mqtt import mqttPublisher
from twisted.python import log
import sys


def main():
    bkr = mqttBroker()
    bkr.run()
    pbr = mqttPublisher()
    pbr.run()


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()