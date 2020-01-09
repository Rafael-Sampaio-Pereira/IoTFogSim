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
	canvas = config()
	load_nodes(canvas)

	
				

			


	#server = StandardServerDevice(canvas)
	#server.run()




	#client = StandardClientDevice(canvas)
	#client.run()
	#ap = AccessPoint(canvas)

	#con1 = Connection(canvas,ap,client)





if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()