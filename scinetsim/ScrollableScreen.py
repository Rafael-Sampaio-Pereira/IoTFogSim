
import tkinter
from tkinter import messagebox
from twisted.python import log
from twisted.internet import reactor

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

        self.canvas.create_text(50,10, anchor="nw", text="Events: ")
        self.events_counter_label = self.canvas.create_text(102,10, anchor="nw", text="0", tags=("events_counter_label",))

        # This is what enables scrolling with the mouse:
        self.canvas.bind("<ButtonPress-2>", self.scroll_start)
        self.canvas.bind("<B2-Motion>", self.scroll_move)

        # Creating top menu
        top_menu = self.create_top_menu(root)

        #Set action to the window close button. - Rafael Sampaio
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Sets esc to close application - Rafael Sampaio
        root.bind('<Escape>', lambda e: self.on_closing())

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
        menubar = tkinter.Menu(window)
        
        mainmenu = tkinter.Menu(menubar, tearoff=0)
        mainmenu.add_command(label="Opção 1", command=None)
        mainmenu.add_separator()  
        mainmenu.add_command(label="Exit", command=self.on_closing)
        
        menubar.add_cascade(label="Main", menu=mainmenu)
        menubar.add_command(label="About Project", command=None)
        menubar.add_command(label="Help", command=None)
        
        window.config(menu=menubar)

    # This method is called when close window button is press. - Rafael Sampaio
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", icon='warning'):
            log.msg("Closing IoTFogSim Application...")
            # window.destroy() # it maybe not need. - Rafael Sampaio
            reactor.stop()