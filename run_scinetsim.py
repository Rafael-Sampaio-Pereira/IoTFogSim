from twisted.internet import reactor
from twisted.python import log
import sys

import tkinter

from twisted.internet import tksupport

from tkinter import messagebox
from tkinter import PhotoImage

from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint

import PIL
from PIL import ImageTk, Image

import random

# These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
window = tkinter.Tk()
tksupport.install(window)

global canvas
canvas = None

class ScrollableScreen(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        self.screen_w = 2000
        self.screen_h = 2000
        
        self.canvas = tkinter.Canvas(self, width= self.screen_w, height= self.screen_h, bg='steelblue', highlightthickness=0)
        self.xsb = tkinter.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,  self.screen_w,  self.screen_h))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

       
        self.canvas.create_text(50,10, anchor="nw", 
                                text="Click and drag to move the canvas")

        # This is what enables scrolling with the mouse:
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)
        

       	global canvas
        canvas = self.canvas
      

    def scroll_start(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_dragto(event.x, event.y, gain=1)




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
		
	# pack allow componentes to be displayed on the main window. - Rafael Sampaio
	#canvas.pack(side=tkinter.RIGHT)

	# Simulation area on screen. - Rafael Sampaio
	ScrollableScreen(window).pack(fill="both", expand=True)
	

def top_menu():
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

	server = StandardServerDevice(canvas)
	server.run()

	client = StandardClientDevice(canvas)
	client.run()
	ap = AccessPoint(canvas)



if __name__ == '__main__':
    log.startLogging(sys.stdout)
    config()
    main()
    reactor.run()