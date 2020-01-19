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




def main():

	config()


	
			




if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()