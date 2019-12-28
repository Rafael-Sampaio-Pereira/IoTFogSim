from twisted.internet import reactor
from twisted.python import log
import sys
import tkinter
from twisted.internet import tksupport
from tkinter import PhotoImage
from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint
from scinetsim.ScrollableScreen import ScrollableScreen
from scinetsim.standarddevice import Connection
import PIL
from PIL import ImageTk, Image
import random



def config():
	# These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
	window = tkinter.Tk()
	tksupport.install(window)

	# Main window size and positions settings. - Rafael Sampaio
	w_heigth = 600
	w_width = 800
	w_top_padding = 80
	w_letf_padding = 100
	window.geometry(str(w_width)+"x"+str(w_heigth)+"+"+str(w_letf_padding)+"+"+str(w_top_padding))

	# Setting window icon. - Rafael Sampaio
	window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='graphics/icons/scinetsim_icon.png'))
	
	# Setting window top text. - Rafael Sampaio
	window.title("IoTFogSim v1.0.1 - An Distributed Event-Driven Network Simulator")
	
	# Simulation area on screen. - Rafael Sampaio
	simulation_screen = ScrollableScreen(window)
	simulation_screen.pack(fill="both", expand=True)
	canvas = simulation_screen.getCanvas()

	return canvas


def main():
	canvas = config()

	server = StandardServerDevice(canvas)
	server.run()

	client = StandardClientDevice(canvas)
	client.run()
	ap = AccessPoint(canvas)

	con1 = Connection(canvas,ap,client)



if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()