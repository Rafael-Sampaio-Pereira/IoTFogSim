

import tkinter
from twisted.internet import tksupport
from config.settings import version
from tkinter import PhotoImage
from twisted.internet.task import LoopingCall
from PIL import ImageTk


class DashboardScreen(tkinter.Frame):
    def __init__(self, project_name, simulation_core):
        self.root = tkinter.Toplevel()
        tksupport.install(self.root)
        w_heigth = 300
        w_width = 700
        w_top_padding = 900
        w_letf_padding = 1000
        self.scrollable_height = w_heigth + 200
        self.scrollable_width = w_width
        self.root.geometry(str(w_width)+"x"+str(w_heigth)+"+" +
                        str(w_letf_padding)+"+"+str(w_top_padding))
        self.root.resizable(False, True)
        self.root.iconify()
        tkinter.Frame.__init__(self, self.root)
        
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen",
                                                            not self.root.attributes("-fullscreen")))
        self.root.iconphoto(True, PhotoImage(
            file='graphics/icons/iotfogsim_icon.png'))
        self.root.title(
            "IoTFogSim %s - An Event-Driven Network Simulator - Dashboard" % (version))
        
        self.root.update()
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
            0, 0,  self.scrollable_width,  self.scrollable_height))

        # self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # This is what enables scrolling with the mouse:
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)
        
        self.all_icons = []
        
        update_interval = 1
        LoopingCall(self.update_dashboard).start(update_interval, now=True)
        
       
    def scroll_start(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    
    def getCanvas(self):
        return self.canvas
    
    def update_dashboard(self):
        before_padding = 10
        last_height = 60

        for index, machine in enumerate(self.simulation_core.all_machines):
            image_file = ImageTk.PhotoImage(file=machine.icon)
            temp_height = image_file.height()+before_padding
            self.scrollable_height += temp_height
            self.canvas.create_image(
                50, last_height, image=image_file, tag="icon")
            self.all_icons.append(image_file)
            last_height += 60
        
        self.canvas.configure(scrollregion=(
            0, 0,  self.scrollable_width,  self.scrollable_height))
        

            
            # self.canvas.columnconfigure(0) # making the columns responsive
            # self.canvas.rowconfigure(index) # making the rows responsive
            # # b = tkinter.Entry(self.root,label=image_file)
            # label = tkinter.Label(self.canvas, image = image_file)
            # label.image = image_file
            # label.grid(row=index,column=0,sticky=tkinter.NSEW)

