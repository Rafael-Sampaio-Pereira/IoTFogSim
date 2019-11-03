from twisted.internet import reactor
from scinetsim.mqtt import mqttBroker
from scinetsim.mqtt import mqttPublisher
from twisted.python import log
import sys

import tkinter

from twisted.internet import tksupport

from tkinter import messagebox

# These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
window = tkinter.Tk()
tksupport.install(window)


window.title("SCINetSim v1.0.1 - An Smart City Integrated Networks Simulator")
# pack is used to show the object in the window
label = tkinter.Label(window, text = "Simulation is ready to play").pack()


# This method is called when close window button is press. - Rafael Sampaio
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        log.msg("Closing SCINetSim Application...")
        # window.destroy() # it maybe not need. - Rafael Sampaio
        reactor.stop()
window.protocol("WM_DELETE_WINDOW", on_closing)
# make Esc exit the program
window.bind('<Escape>', lambda e: reactor.stop())

# create a menu bar with an Exit command
menubar = tkinter.Menu(window)
mainmenu = tkinter.Menu(menubar, tearoff=0)

mainmenu.add_command(label="Exit", command=reactor.stop)
menubar.add_cascade(label="Main", menu=mainmenu)

menubar.add_command(label="About Project", command=reactor.stop)
window.config(menu=menubar)


def main():
    bkr = mqttBroker()
    bkr.run()
    pbr = mqttPublisher()
    pbr.run()


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()

    reactor.run()
    #window.mainloop()