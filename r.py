from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.task import deferLater


def sleep(secs):
    return deferLater(reactor, secs, lambda: None)


@inlineCallbacks
def f():
    print('writing for 5 seconds ...')
    yield sleep(0.5)
    print('now i am back ...')


f()

reactor.callLater(6, reactor.stop)
reactor.run()
