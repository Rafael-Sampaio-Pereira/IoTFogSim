

import tkinter
from twisted.internet import tksupport
from config.settings import version
from tkinter import PhotoImage


class DashboardScreen(tkinter.Frame):
    def __init__(self, project_name, simulation_core):
        root = tkinter.Toplevel()
        tksupport.install(root)
        w_heigth = 300
        w_width = 700
        w_top_padding = 900
        w_letf_padding = 1000
        self.scrollable_height = w_heigth + 200
        root.geometry(str(w_width)+"x"+str(w_heigth)+"+" +
                        str(w_letf_padding)+"+"+str(w_top_padding))
        root.resizable(False, True)
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
        self.canvas.simulation_core = simulation_core
        self.simulation_core = simulation_core
        
        # self.xsb = tkinter.Scrollbar(
        #     self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tkinter.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set,
                              xscrollcommand=None)
        self.canvas.configure(scrollregion=(
            0, 0,  w_width,  self.scrollable_height))

        # self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # self.canvas.create_text(50,10, anchor="nw", text="Events: ")
        # self.events_counter_label = self.canvas.create_text(102,10, anchor="nw", text="0", tags=("events_counter_label",))

        # # Label to show position on screen - Rafael Sampaio
        # self.position_label = self.canvas.create_text(300,10, anchor="nw", text="0", tags=("position_label",))

        # This is what enables scrolling with the mouse:
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)
        
        self.ball = self.canvas.create_oval(100, 400, 150, 450, fill="red")
        
    def scroll_start(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    
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
