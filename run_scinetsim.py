from twisted.internet import reactor
from scinetsim.mqtt import mqttBroker
from scinetsim.mqtt import mqttPublisher
from twisted.python import log
import sys

import tkinter

from twisted.internet import tksupport

from tkinter import messagebox
from tkinter import PhotoImage

from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice

import PIL
from PIL import ImageTk, Image

# These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
window = tkinter.Tk()
tksupport.install(window)

top_frame = tkinter.Frame(window).pack()

global canvas
canvas = None

# This method is called when close window button is press. - Rafael Sampaio
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        log.msg("Closing SCINetSim Application...")
        # window.destroy() # it maybe not need. - Rafael Sampaio
        reactor.stop()

def config():
	# Main window size and positions settings. - Rafael Sampaio
	w_heigth = 600
	w_width = 800
	w_top_padding = 80
	w_letf_padding = 100
	window.geometry(str(w_width)+"x"+str(w_heigth)+"+"+str(w_letf_padding)+"+"+str(w_top_padding))

	# Setting window icon. - Rafael Sampaio
	window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='graphics/icons/scinetsim_icon.png'))
	
	# Setting window top text. - Rafael Sampaio
	window.title("SCINetSim v1.0.1 - An Smart City Integrated Network Simulator")
	
	#Set action to the window close button. - Rafael Sampaio
	window.protocol("WM_DELETE_WINDOW", on_closing)
	
	# Sets esc to close application - Rafael Sampaio
	window.bind('<Escape>', lambda e: on_closing())
	
	global canvas
	canvas = tkinter.Canvas(top_frame, width=1000, height=900, bg='steelblue', highlightthickness=0)
	# pack allow componentes to be displayed on the main window. - Rafael Sampaio
	canvas.pack(side=tkinter.RIGHT)
	#canvas.pack(fill="both", expand=True)


def top_menu():
	# create a menu bar with an Exit command
	menubar = tkinter.Menu(window)
	mainmenu = tkinter.Menu(menubar, tearoff=0)
	mainmenu.add_command(label="Opção 1", command=None)
	mainmenu.add_separator()  
	mainmenu.add_command(label="Exit", command=on_closing)
	menubar.add_cascade(label="Main", menu=mainmenu)

	menubar.add_command(label="About Project", command=None)
	menubar.add_command(label="Help", command=None)
	window.config(menu=menubar)


def main():
	global canvas
	top_menu()

	server = StandardServerDevice()
	server.setCanvas(canvas)
	server.run()
	client = StandardClientDevice()
	client.setCanvas(canvas)
	client.run()




if __name__ == '__main__':
    log.startLogging(sys.stdout)
    config()
    main()

    reactor.run()
    #window.mainloop()
