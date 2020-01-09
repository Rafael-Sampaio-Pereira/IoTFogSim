import tkinter
from tkinter import PhotoImage
from twisted.internet import tksupport
from scinetsim.ScrollableScreen import ScrollableScreen

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
	window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))
	
	# Setting window top text. - Rafael Sampaio
	window.title("IoTFogSim v1.0.1 - An Distributed Event-Driven Network Simulator")
	
	# Simulation area on screen. - Rafael Sampaio
	simulation_screen = ScrollableScreen(window)
	simulation_screen.pack(fill="both", expand=True)
	canvas = simulation_screen.getCanvas()

	return canvas