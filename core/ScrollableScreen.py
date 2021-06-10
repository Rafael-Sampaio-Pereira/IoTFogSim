
import tkinter
from tkinter import messagebox
from twisted.python import log
from twisted.internet import reactor
from tkinter import ALL, EventType
import datetime
from datetime import datetime
from twisted.internet import tksupport
import os.path
from config.settings import version
import PIL
from PIL import Image, ImageTk
from tkinter import PhotoImage


class ScrollableScreen(tkinter.Frame):
    def __init__(self, root, project_name, resizeable):
        tkinter.Frame.__init__(self, root)

        bg_width = None
        bg_height = None
        background_image = None

        bg_image_path = "projects/"+project_name+"/bg_image.png"
        
        # verify if the bg image exists - Rafael Sampaio
        if os.path.isfile(bg_image_path):
            background_image = PIL.Image.open(bg_image_path)
            bg_width, bg_height = background_image.size
        
        root.update()

        self.screen_w = bg_width or 2000
        self.screen_h = bg_height or 2000

        
        # Resize the image to the constraints of the root window.
        win_width = int(root.winfo_width())
        win_height = int(root.winfo_height())


        if background_image:
            background_image_tk = ImageTk.PhotoImage(background_image)

        if resizeable == False:
            # configure window to the bg image size and desable the resize funciton - Rafael Sampaio
            root.geometry(str(self.screen_w)+"x"+str(self.screen_h))
            root.resizable(False, False)
        
        
        self.canvas = tkinter.Canvas(self, width= self.screen_w, height= self.screen_h, bg='#159eba', highlightthickness=0)


        # Create a label to hold the background image.
        if background_image:
            self.canvas.place(x=0, y=0, anchor='nw')
            self.canvas.create_image(0, 0, image=background_image_tk, anchor='nw')
            self.canvas.image = background_image_tk



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

        # Creating context menu - Rafael Sampaio
        self.create_context_menu()

    def create_context_menu(self):
        
        self.contextMenu = tkinter.Menu(self, tearoff=0)
        self.contextMenu.config(bg="#99ccff", fg="black", activebackground='#3399ff', activeforeground="whitesmoke", activeborderwidth=1, font="Monaco 11")

        cloudMenu = tkinter.Menu(self.contextMenu, tearoff=0)
        cloudMenu.config(bg="white", fg="black", activebackground="#3399ff", activeforeground="whitesmoke", font="Monaco 11")
        cloudMenu.add_command(label="New Server", command=lambda:self.add_new_node_modal_screen('cloud','server'))
        cloudMenu.add_command(label="New Client", command=lambda:self.add_new_node_modal_screen('cloud','client'))
        cloudMenu.add_command(label="New Router", command=lambda:self.add_new_node_modal_screen('cloud','router'))
        cloudMenu.add_command(label="New Access Point", command=lambda:self.add_new_node_modal_screen('cloud','access_point'))
        cloudMenu.add_command(label="New Wireless Computer", command=lambda:self.add_new_node_modal_screen('cloud','wireless_computer'))


        fogMenu = tkinter.Menu(self.contextMenu, tearoff=0)
        fogMenu.config(bg="white", fg="black", activebackground="#3399ff", activeforeground="whitesmoke", font="Monaco 11")
        fogMenu.add_command(label="New Server", command=lambda:self.add_new_node_modal_screen('fog','server'))
        fogMenu.add_command(label="New Client", command=lambda:self.add_new_node_modal_screen('fog','client'))
        fogMenu.add_command(label="New Router", command=lambda:self.add_new_node_modal_screen('fog','router'))
        fogMenu.add_command(label="New Access Point", command=lambda:self.add_new_node_modal_screen('fog','access_point'))
        fogMenu.add_command(label="New Wireless Computer", command=lambda:self.add_new_node_modal_screen('fog','wireless_computer'))


        iotMenu = tkinter.Menu(self.contextMenu, tearoff=0)
        iotMenu.config(bg="white", fg="black", activebackground="#3399ff", activeforeground="whitesmoke", font="Monaco 11")
        iotMenu.add_command(label="New Server", command=lambda:self.add_new_node_modal_screen('iot','server'))
        iotMenu.add_command(label="New Client", command=lambda:self.add_new_node_modal_screen('iot','client'))
        iotMenu.add_command(label="New Router", command=lambda:self.add_new_node_modal_screen('iot','router'))
        iotMenu.add_command(label="New Access Point", command=lambda:self.add_new_node_modal_screen('iot','access_point'))
        iotMenu.add_command(label="New Wireless Computer", command=lambda:self.add_new_node_modal_screen('iot','wireless_computer'))



        self.contextMenu.add_cascade(label="Add Cloud node", menu=cloudMenu)
        self.contextMenu.add_cascade(label="Add Fog node", menu=fogMenu)
        self.contextMenu.add_cascade(label="Add IoT node", menu=iotMenu)
        

        #  self.contextMenu.add_command(label="Add Cloud node", activebackground='#3399ff', activeforeground="white", command=self.add_cloud_menu)
        # self.contextMenu.add_command(label="Add Fog node",  command=self.add_fog_menu)
        # self.contextMenu.add_command(label="Add IoT node", activebackground='#3399ff', activeforeground="white", command=self.add_iot_menu)
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label="Close", compound = tkinter.CENTER, activebackground='#ff4d4d', activeforeground="white", font=("Monaco", 11, "bold"), command=self.closeContextMenu)
        self.contextMenu.entryconfig(4, foreground='#b30000')

        # Configure context menu on rigth click - Rafael Sampaio
        self.canvas.bind("<Button-3>", self.openContextMenu)
        
    # Context menu functions - Rafael Sampaio
    def openContextMenu(self, event):
        self.contextMenu.post(event.x_root, event.y_root)
    
    def closeContextMenu(self, event):
        pass


    def add_new_node_modal_screen(self,network_layer, node_type):
        window = tkinter.Toplevel()
        tksupport.install(window)
        window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
        window.geometry("400x551")
        window.resizable(False, False)

        # Setting window icon. - Rafael Sampaio
        window.iconphoto(True, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))

        if network_layer == 'cloud':
            if node_type == 'server':
                print('Adding new server in Cloud layer...')
            elif node_type == 'client':
                print('Adding new client in Cloud layer...')
            elif node_type == 'router':
                print('Adding new router in Cloud layer...')
            elif node_type == 'access_point':
                print('Adding new access point in Cloud layer...')
            elif node_type == 'wireless_computer':
                print('Adding new wireless computer in Cloud layer...')
            else:
                print('Unknow node type.')
        elif network_layer == 'fog':
            if node_type == 'server':
                print('Adding new server in Fog layer...')
            elif node_type == 'client':
                print('Adding new client in Fog layer...')
            elif node_type == 'router':
                print('Adding new router in Fog layer...')
            elif node_type == 'access_point':
                print('Adding new access point in Fog layer...')
            elif node_type == 'wireless_computer':
                print('Adding new wireless computer in Fog layer...')
            else:
                print('Unknow node type.')
        elif network_layer == 'iot':
            if node_type == 'server':
                print('Adding new server in IoT layer...')
            elif node_type == 'client':
                print('Adding new client in IoT layer...')
            elif node_type == 'router':
                print('Adding new router in IoT layer...')
            elif node_type == 'access_point':
                print('Adding new access point in IoT layer...')
            elif node_type == 'wireless_computer':
                print('Adding new wireless computer in IoT layer...')
            else:
                print('Unknow node type.')
        else:
            print('Unknow network layer.')

        


        

        
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
        # sertting the coordinates to canvas relative. by default it is window realative and don't change when window is scrolled - Rafael Sampaio
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        p = "Position: "+str(x)+' x '+str(y)

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
        if messagebox.askokcancel("Quit", "Do you really want to quit?", icon='warning'):
            log.msg("Closing IoTFogSim Application...")
            # window.destroy() # it maybe not need. - Rafael Sampaio
            # reactor.stop()
            reactor.crash()