from twisted.internet import reactor
from twisted.python import log
import sys
import tkinter
from tkinter import PhotoImage

import PIL
from PIL import ImageTk, Image
import random

from scinetsim.configurations import config
from scinetsim.configurations import  load_nodes

from sys import stdout
from twisted.logger import Logger, textFileLogObserver, globalLogBeginner

def main():

	config()


if __name__ == '__main__':
    # log.discardLogs()
    # log.startLogging(sys.stdout)
    # start the global logger
    logfile = open('log.log', 'a')
    globalLogBeginner.beginLoggingTo([
        textFileLogObserver(stdout),
        textFileLogObserver(logfile)])

    log = Logger()
    # log.info('hello world')
    # log.debug('hello world')
    main()
    reactor.run()