

import tkinter
from twisted.internet import tksupport
from config.settings import version
from tkinter import PhotoImage


class DashboardScreen(tkinter.Frame):
    def __init__(self, project_name, simulation_core):
        root = tkinter.Toplevel()
        tksupport.install(root)
        root.geometry("700x900")
        root.resizable(False, False)
        root.iconify()
        tkinter.Frame.__init__(self, root)
        
        root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                                            not root.attributes("-fullscreen")))
        root.iconphoto(True, PhotoImage(
            file='graphics/icons/iotfogsim_icon.png'))
        root.title(
            "IoTFogSim %s - An Event-Driven Network Simulator - Dashboard" % (version))
        
        root.update()
        self.canvas = tkinter.Canvas(
            self, width=500, height=400, bg='#263238', highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.simulation_core = simulation_core
        
        self.ball = self.canvas.create_oval(10, 10, 40, 40, fill="black")
    
    def getCanvas(self):
        return self.canvas
        


# def dashboard(self):
#     window = tkinter.Toplevel()
#     tksupport.install(window)
#     window.title(
#         "IoTFogSim %s - An Event-Driven Network Simulator - Dashboard" % (version))
#     window.geometry("700x900")
#     window.resizable(False, True)

#     # Setting window icon. - Rafael Sampaio
#     window.iconphoto(True, PhotoImage(
#         file='graphics/icons/iotfogsim_icon.png'))
    

#     self.dashboard_canvas = tkinter.Canvas(
#         window, width=500, height=400, bg='#263238', highlightthickness=0)
