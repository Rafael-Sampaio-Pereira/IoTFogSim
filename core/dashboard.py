

import tkinter
from twisted.internet import tksupport
from config.settings import version
from tkinter import PhotoImage
from twisted.internet.task import LoopingCall
from PIL import ImageTk
from tkinter import ttk
import datetime
from twisted.internet import reactor


class DashboardScreen(tkinter.Frame):
    def __init__(self, project_name, simulation_core):
        self.root = tkinter.Toplevel()
        tksupport.install(self.root)
        self.w_heigth = 300
        self.w_width = 700
        w_top_padding = 900
        w_letf_padding = 1000
        self.scrollable_height = self.w_heigth
        self.scrollable_width = self.w_width
        self.root.geometry(str(self.w_width)+"x"+str(self.w_heigth)+"+" +
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
        
        self.update_interval = 1
        LoopingCall(self.update_dashboard).start(self.update_interval, now=True)
        
       
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
        self.all_icons = []
        self.scrollable_height = self.w_heigth
        for index, machine in enumerate(self.simulation_core.all_machines):
            image_file = ImageTk.PhotoImage(file=machine.icon)
            temp_height = image_file.height()+before_padding
            self.scrollable_height += temp_height
            icon = self.canvas.create_image(
                50, last_height, image=image_file, tag="icon")
            self.all_icons.append(image_file)
            
            _type = self.canvas.create_text(120, last_height-10, anchor="nw", text=f"{machine.type}" if len(machine.type) <= 6 else f"{machine.type[:4 or None]}...", fill="white")
            ip = self.canvas.create_text(170, last_height-10, anchor="nw", text=f"{machine.network_interfaces[0].ip}", fill="white")
            power = self.canvas.create_text(265, last_height-10, anchor="nw", text=f"{machine.power_watts}W", fill="white")
            kwh = self.canvas.create_text(320, last_height-10, anchor="nw", text=f"{machine.get_consumed_energy()}", fill="white")
            state = None

            if machine.is_turned_on:
                state = self.canvas.create_text(420, last_height-10, anchor="nw", text=f"ON", fill="green", font='bold')
            else:
                state = self.canvas.create_text(420, last_height-10, anchor="nw", text=f"OFF", fill="red", font='bold')
            
            up_time = self.canvas.create_text(460, last_height-10, anchor="nw", text=f"{str(datetime.timedelta(seconds=machine.up_time))}", fill="white")
            billing_amount = self.canvas.create_text(520, last_height-10, anchor="nw", text=f"{machine.get_billable_amount()}", fill="white")
            
            line = self.canvas.create_line(0,last_height+30,self.w_width,last_height+30, width=1, fill="#37474F")
            line2 = self.canvas.create_line(0,last_height+31,self.w_width,last_height+31, width=1, fill="#212121")
            
            
            last_height += 60
            
            # delete old displayed items
            reactor.callLater(self.update_interval, self.canvas.delete, _type)
            reactor.callLater(self.update_interval, self.canvas.delete, icon)
            reactor.callLater(self.update_interval, self.canvas.delete, ip)
            reactor.callLater(self.update_interval, self.canvas.delete, kwh)
            reactor.callLater(self.update_interval, self.canvas.delete, power)
            reactor.callLater(self.update_interval, self.canvas.delete, state)
            reactor.callLater(self.update_interval, self.canvas.delete, up_time)
            reactor.callLater(self.update_interval, self.canvas.delete, billing_amount)
            reactor.callLater(self.update_interval, self.canvas.delete, line)
            reactor.callLater(self.update_interval, self.canvas.delete, line2)
        
        
        self.canvas.configure(scrollregion=(
            0, 0,  self.scrollable_width,  self.scrollable_height))
        

            
            # self.canvas.columnconfigure(0) # making the columns responsive
            # self.canvas.rowconfigure(index) # making the rows responsive
            # # b = tkinter.Entry(self.root,label=image_file)
            # label = tkinter.Label(self.canvas, image = image_file)
            # label.image = image_file
            # label.grid(row=index,column=0,sticky=tkinter.NSEW)

