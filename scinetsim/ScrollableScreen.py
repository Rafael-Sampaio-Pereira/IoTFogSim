
import tkinter
from tkinter import messagebox
from twisted.python import log
from twisted.internet import reactor
from tkinter import ALL, EventType
import datetime
from datetime import datetime


class ScrollableScreen(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root)

        self.screen_w = 2000
        self.screen_h = 2000
        
        
        self.canvas = tkinter.Canvas(self, width= self.screen_w, height= self.screen_h, bg='#159eba', highlightthickness=0)
        self.xsb = tkinter.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,  self.screen_w,  self.screen_h))

        self.xsb.grid(row=1, column=0, sticky="ew")
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

        # Creating top menu
        top_menu = self.create_top_menu(root)

        #Set action to the window close button. - Rafael Sampaio
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Sets esc to close application - Rafael Sampaio
        root.bind('<Escape>', lambda e: self.on_closing())


        root.bind("<Motion>", self.update_position_on_screen)

        
    # AS LINHAS ABAIXO SERÃO UTEIS NO CÓDIGO DE ZOOM
        
    #     #linux scroll
    #     self.canvas.bind("<Button-4>", self.zoomerP)
    #     self.canvas.bind("<Button-5>", self.zoomerM)
    #     #windows scroll
    #     self.canvas.bind("<MouseWheel>",self.zoomer)

    # #linux zoom
    # def zoomerP(self,event):
    #     self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
    #     self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    # def zoomerM(self,event):
    #     self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
    #     self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    # #windows zoom
    # def zoomer(self,event):
    #     if (event.delta > 0):
    #         self.canvas.scale(ALL, event.x, event.y, 1.1, 1.1)
    #     elif (event.delta < 0):
    #         self.canvas.scale(ALL, event.x, event.y, 0.9, 0.9)
    #     self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    


    def  update_position_on_screen(self,event):
        p = "Position: "+str(event.x)+'x'+str(event.y)
        # self.canvas.itemconfig(self.position_label, text=p)
        self.menubar.entryconfigure(4, label=p)

    def getCanvas(self):
     	return self.canvas

    def scroll_start(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.config(cursor='fleur')
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def create_top_menu(self, window):
        # 'window' param is the 'root' param in ScrollableScreen __init__ method - Rafael Sampaio
        self.menubar = tkinter.Menu(window)
        
        mainmenu = tkinter.Menu(self.menubar, tearoff=0)
        mainmenu.add_command(label="Opção 1", command=None)
        mainmenu.add_separator()  
        mainmenu.add_command(label="Exit", command=self.on_closing)

        self.menubar.add_cascade(label="Main", menu=mainmenu)
        self.menubar.add_command(label="About Project", command=None)
        self.menubar.add_command(label="Help", command=None)
        
        self.menubar.add_command(label="Position: 0", command=None)
        self.menubar.add_command(label=" Events:", command=None)

        self.menubar.add_command(label="Start Time: "+str(datetime.now().strftime('%H:%M:%S')), font=("Verdana", 10, "italic"), command=None)

        self.menubar.entryconfig(4, foreground='blue')
        self.menubar.entryconfig(5, foreground='blue')

        window.config(menu=self.menubar)

    # This method is called when close window button is press. - Rafael Sampaio
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", icon='warning'):
            log.msg("Closing IoTFogSim Application...")
            # window.destroy() # it maybe not need. - Rafael Sampaio
            reactor.stop()