
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
from core.functions import get_all_app_classes_name
from tkinter import ttk
import pathlib
from tkinter import filedialog
from random import randrange
from core.addNewNodeModal import add_new_node_modal_screen
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep

class ScrollableScreen(tkinter.Frame):
    def __init__(self, root, project_name, resizeable, simulation_core):
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

        self.canvas = tkinter.Canvas(
            self, width=self.screen_w, height=self.screen_h, bg='#ceebe3', highlightthickness=0)
        self.canvas.simulation_core = simulation_core

        # Create a label to hold the background image.
        if background_image:
            self.canvas.place(x=0, y=0, anchor='nw')
            self.canvas.create_image(
                0, 0, image=background_image_tk, anchor='nw')
            self.canvas.image = background_image_tk

        self.xsb = tkinter.Scrollbar(
            self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tkinter.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set,
                              xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(
            0, 0,  self.screen_w,  self.screen_h))

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

        # Set action to the window close button. - Rafael Sampaio
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Sets esc to close application - Rafael Sampaio
        root.bind('<Escape>', lambda e: self.on_closing())

        root.bind("<Motion>", self.update_position_on_screen)

        # Creating context menu - Rafael Sampaio
        self.create_context_menu()

    def create_context_menu(self):
        if self.canvas.simulation_core.is_running == False:

            self.contextMenu = tkinter.Menu(self, tearoff=0)
            self.contextMenu.config(bg="#99ccff", fg="black", activebackground='#3399ff',
                                    activeforeground="whitesmoke", activeborderwidth=1, font="Monaco 11")

            cloudMenu = tkinter.Menu(self.contextMenu, tearoff=0)
            cloudMenu.config(bg="white", fg="black", activebackground="#3399ff",
                             activeforeground="whitesmoke", font="Monaco 11")
            cloudMenu.add_command(label="New Server", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'cloud', 'server'))
            cloudMenu.add_command(label="New Client", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'cloud', 'client'))
            cloudMenu.add_command(label="New Router", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'cloud', 'router'))
            # cloudMenu.add_command(label="New Access Point", command=lambda:add_new_node_modal_screen(self.canvas.simulation_core,'cloud','access_point'))
            cloudMenu.add_command(label="New Wireless Computer", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'cloud', 'wireless_computer'))

            fogMenu = tkinter.Menu(self.contextMenu, tearoff=0)
            fogMenu.config(bg="white", fg="black", activebackground="#3399ff",
                           activeforeground="whitesmoke", font="Monaco 11")
            fogMenu.add_command(label="New Server", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'fog', 'server'))
            fogMenu.add_command(label="New Client", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'fog', 'client'))
            fogMenu.add_command(label="New Router", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'fog', 'router'))
            # fogMenu.add_command(label="New Access Point", command=lambda:add_new_node_modal_screen(self.canvas.simulation_core,'fog','access_point'))
            fogMenu.add_command(label="New Wireless Computer", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'fog', 'wireless_computer'))

            iotMenu = tkinter.Menu(self.contextMenu, tearoff=0)
            iotMenu.config(bg="white", fg="black", activebackground="#3399ff",
                           activeforeground="whitesmoke", font="Monaco 11")
            iotMenu.add_command(label="New Server", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'iot', 'server'))
            iotMenu.add_command(label="New Client", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'iot', 'client'))
            iotMenu.add_command(label="New Router", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'iot', 'router'))
            # iotMenu.add_command(label="New Access Point", command=lambda:add_new_node_modal_screen(self.canvas.simulation_core,'iot','access_point'))
            iotMenu.add_command(label="New Wireless Computer", command=lambda: add_new_node_modal_screen(
                self.canvas.simulation_core, 'iot', 'wireless_computer'))

            self.contextMenu.add_cascade(
                label="Add Cloud node", menu=cloudMenu)
            self.contextMenu.add_cascade(label="Add Fog node", menu=fogMenu)
            self.contextMenu.add_cascade(label="Add IoT node", menu=iotMenu)

            #  self.contextMenu.add_command(label="Add Cloud node", activebackground='#3399ff', activeforeground="white", command=self.add_cloud_menu)
            # self.contextMenu.add_command(label="Add Fog node",  command=self.add_fog_menu)
            # self.contextMenu.add_command(label="Add IoT node", activebackground='#3399ff', activeforeground="white", command=self.add_iot_menu)
            self.contextMenu.add_separator()
            self.contextMenu.add_command(label="Close", compound=tkinter.CENTER, activebackground='#ff4d4d',
                                         activeforeground="white", font=("Monaco", 11, "bold"), command=self.closeContextMenu)
            self.contextMenu.entryconfig(4, foreground='#b30000')

            # Configure context menu on rigth click - Rafael Sampaio
            self.canvas.bind("<Button-3>", self.openContextMenu)

    # Context menu functions - Rafael Sampaio
    def openContextMenu(self, event):
        if self.canvas.simulation_core.is_running == False:
            self.contextMenu.post(event.x_root, event.y_root)

    def closeContextMenu(self, event):
        pass

    # def add_new_node_modal_screen(self, network_layer, node_type):
    #     window = tkinter.Toplevel()
    #     tksupport.install(window)
    #     window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
    #     window.geometry("400x551")
    #     window.resizable(False, False)

    #     # Setting window icon. - Rafael Sampaio
    #     window.iconphoto(True, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))

    #     # hearder message - Rafael Sampaio
    #     create_msg = tkinter.Label(window,text="Create new "+node_type.replace("_"," ")+" at "+network_layer+" layer.")
    #     create_msg.place(relx="0.1",rely="0.05")

    #     # New node Name - Rafael Sampaio
    #     name_label = tkinter.Label(window,text="Name:")
    #     name_label.place(relx="0.1",rely="0.12")
    #     input_name = tkinter.Entry(window)
    #     input_name.place(relx="0.25",rely="0.12")

    #     # New node position on screen -Rafael Sampaio
    #     create_msg = tkinter.Label(window,text="Position:")
    #     create_msg.place(relx="0.1",rely="0.18")
    #     x = window.winfo_pointerx()
    #     y = window.winfo_pointery()
    #     x_label = tkinter.Label(window,text="X")
    #     x_label.place(relx="0.25",rely="0.18")
    #     input_x = tkinter.Entry(window)
    #     input_x.insert(-1, x)
    #     input_x.place(width="35", relx="0.29", rely="0.18")
    #     y_label = tkinter.Label(window, text="Y")
    #     y_label.place(relx="0.45",rely="0.18")
    #     input_y = tkinter.Entry(window)
    #     input_y.insert(-1, y)
    #     input_y.place(width="35", relx="0.49",rely="0.18")

    #     # input for new node coverage area, deafult is disabled - Rafael Sampaio
    #     coverage_area_label = tkinter.Label(window,text="Coverage area:")
    #     coverage_area_label.place(relx="0.1",rely="0.30")
    #     input_coverage_area = tkinter.Entry(window, state='disabled')
    #     input_coverage_area.place(width="124", relx="0.35",rely="0.30")

    #     # controller for radio buttons that enable and disable the coverage are input - Rafael Sampaio
    #     radio_button_controller = tkinter.IntVar()

    #     # function to enable coverage area input - Rafael Sampaio
    #     def enableCoverage():
    #         input_coverage_area.configure(state="normal")
    #         input_coverage_area.update()
    #     # function to desable coverage area input - Rafael Sampaio
    #     def disableCoverage():
    #         input_coverage_area.configure(state="disabled")
    #         input_coverage_area.update()

    #     # radio buttons that enable and disable the coverage area input - Rafael Sampaio
    #     is_wireless_msg = tkinter.Label(window,text="Is wireless?")
    #     is_wireless_msg.place(relx="0.1",rely="0.24")
    #     yes_button = tkinter.Radiobutton(window, text="Yes", variable=radio_button_controller, value="0", command=enableCoverage)
    #     yes_button.place(relx="0.3",rely="0.24")
    #     no_button = tkinter.Radiobutton(window, text="No", variable=radio_button_controller, value="1", command=disableCoverage)
    #     no_button.place(relx="0.45",rely="0.24")

    #     # geting all apps in 'plications' folder files - Rafael Sampaio
    #     all_apps_list = get_all_app_classes_name()

    #     # combox for apps list - Rafael Sampaio
    #     all_app_list_label = tkinter.Label(window,text="App:")
    #     all_app_list_label.place(relx="0.1",rely="0.36")
    #     cmb_app_list = ttk.Combobox(window, width="21", values=all_apps_list)
    #     cmb_app_list.place(relx="0.2",rely="0.36")

    #     # label for the new node icon - Rafael Sampaio
    #     img = Image.open(str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_server.png')
    #     img = img.resize((32, 32))
    #     photo = ImageTk.PhotoImage(img)
    #     icon_label = tkinter.Label(window, image=photo)
    #     icon_label.image = photo
    #     icon_label.place(relx="0.5",rely="0.42")

    #     # function to allow the user choose another icon - Rafael Sampaio
    #     def chooseIconDialog():
    #         path = str(pathlib.Path.cwd())+'/graphics/icons/'
    #         filename = filedialog.askopenfilename(initialdir = path, title = "Choose a icon file", filetypes =
    #         [("png files","*.png")])
    #         img = Image.open(filename)
    #         img = img.resize((32, 32))
    #         photo = ImageTk.PhotoImage(img)
    #         icon_label.configure(image=photo)
    #         icon_label.image = photo
    #         icon_label.update()

    #     # button for choose another icon - Rafael Sampaio
    #     choose_icon_button = ttk.Button(window, text = "Choose another icon",command = chooseIconDialog)
    #     choose_icon_button.place(relx="0.1",rely="0.42")

    #     # just a screen separator - Rafael Sampaio
    #     sep = ttk.Separator(window).place(relx="0.0", rely="0.50", relwidth=1)

    #     # atributtes only for routers, clients and servers - Rafael Sampaio
    #     if (node_type == 'router' or node_type == 'client' or node_type == 'server'):
    #         # New node real ip addr - Rafael Sampaio
    #         real_ip_label = tkinter.Label(window,text="Real IP:")
    #         real_ip_label.place(relx="0.1",rely="0.54")
    #         input_real_ip = tkinter.Entry(window)
    #         input_real_ip.insert(-1, '127.0.0.1')
    #         input_real_ip.place(relx="0.25",rely="0.54")

    #     # atributtes only for routers and servers - Rafael Sampaio
    #     if (node_type == 'router' or node_type == 'server'):
    #         # New node port - Rafael Sampaio
    #         port_label = tkinter.Label(window,text="Port:")
    #         port_label.place(relx="0.1",rely="0.60")
    #         input_port = tkinter.Entry(window)
    #         input_port.insert(-1, str(randrange(8000, 8999)))
    #         input_port.place(width="50",relx="0.25",rely="0.60")

    #     # atributtes only for routers - Rafael Sampaio
    #     if (node_type == 'router'):

    #         def openAPWindow():
    #             ap_window = tkinter.Toplevel()
    #             tksupport.install(ap_window)
    #             ap_window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
    #             ap_window.geometry("300x200")
    #             ap_window.resizable(False, False)

    #             # access point hearder message - Rafael Sampaio
    #             create_msg = tkinter.Label(ap_window,text="Access Point Info")
    #             create_msg.place(relx="0.1",rely="0.05")

    #             # input for router access point addr- Rafael Sampaio
    #             ap_real_ip_label = tkinter.Label(ap_window,text="Real IP:")
    #             ap_real_ip_label.place(relx="0.1",rely="0.20")
    #             input_ap_real_ip = tkinter.Entry(ap_window)
    #             input_ap_real_ip.insert(-1, '127.0.0.1')
    #             input_ap_real_ip.place(relx="0.25", rely="0.20")

    #             # input for router access point port - Rafael Sampaio
    #             ap_port_label = tkinter.Label(ap_window,text="Port:")
    #             ap_port_label.place(relx="0.1",rely="0.35")
    #             ap_input_port = tkinter.Entry(ap_window)
    #             ap_input_port.insert(-1, str(randrange(8000, 8999)))
    #             ap_input_port.place(width="50",relx="0.25",rely="0.35")

    #             # access position on screen -Rafael Sampaio
    #             ap_msg = tkinter.Label(ap_window,text="Position:")
    #             ap_msg.place(relx="0.1",rely="0.50")
    #             ap_x_label = tkinter.Label(ap_window,text="X")
    #             ap_x_label.place(relx="0.25",rely="0.50")
    #             ap_input_x = tkinter.Entry(ap_window)
    #             ap_input_x.insert(-1, int(x)+10)
    #             ap_input_x.place(width="35", relx="0.29", rely="0.50")
    #             ap_y_label = tkinter.Label(ap_window, text="Y")
    #             ap_y_label.place(relx="0.45",rely="0.50")
    #             ap_input_y = tkinter.Entry(ap_window)
    #             ap_input_y.insert(-1, int(y)+10)
    #             ap_input_y.place(width="35", relx="0.49",rely="0.50")

    #             # button to save access point - Rafael Sampaio
    #             save_ap_button = ttk.Button(ap_window, text = "Save", command = None)
    #             save_ap_button.place(relx="0.35",rely="0.70")

    #         # button to open a modal to create access point - Rafael Sampaio
    #         ap_button = ttk.Button(window, text = "Add Access Point", command = openAPWindow)
    #         ap_button.place(relx="0.1",rely="0.66")

    #     # button to save the new node - Rafael Sampaio
    #     save_node_button = ttk.Button(window, text = "Save", command = None)
    #     save_node_button.place(relx="0.4",rely="0.90")

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

    def update_position_on_screen(self, event):
        # sertting the coordinates to canvas relative. by default it is window realative and don't change when window is scrolled - Rafael Sampaio
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        p = "Position: "+str(x)+' x '+str(y)

        self.menubar.entryconfigure(3, label=p)

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

        self.playmenu = tkinter.Menu(self.menubar, tearoff=0)
        play_icon = PIL.Image.open('graphics/icons/iotfogsim_play.png')
        play_icon = play_icon.resize((17, 17), Image.ANTIALIAS)
        play_icon = ImageTk.PhotoImage(play_icon)
        self.menubar.add_command(
            image=play_icon, compound="center", command=self.play_or_stop_simulation)
        self.menubar.iconPhotoImage = play_icon

        self.menubar.add_command(label="Position: 0", command=None)
        self.menubar.add_command(label=" Events:", command=None)

        self.start_time = '--:--:--'

        self.menubar.add_command(
            label="Start Time: "+self.start_time, font=("Verdana", 10, "italic"), command=None)

        self.menubar.entryconfig(3, foreground='blue')
        self.menubar.entryconfig(4, foreground='blue')

        self.menubar.add_command(label="About Project", command=None)
        self.menubar.add_command(label="Help", command=None)

        window.config(menu=self.menubar)

    # @inlineCallbacks
    def play_or_stop_simulation(self):
        is_running = self.canvas.simulation_core.is_running

        if is_running == True:
            log.msg("Info :  - | Stoping simulation...")
            self.canvas.simulation_core.is_running = False
            play_icon = PIL.Image.open('graphics/icons/iotfogsim_play.png')
            play_icon = play_icon.resize((17, 17), Image.ANTIALIAS)
            play_icon = ImageTk.PhotoImage(play_icon)
            self.menubar.entryconfig(2, image=play_icon)
            self.menubar.iconPhotoImage = play_icon
            self.on_closing()
        elif is_running == False:
            if self.start_time == '--:--:--':
                self.start_time = str(datetime.now().strftime('%H:%M:%S'))
                self.menubar.entryconfig(
                    5, label="Start Time: "+self.start_time)

            log.msg("Info : - | Starting simulation...")
            self.canvas.simulation_core.is_running = True

            stop_icon = PIL.Image.open('graphics/icons/iotfogsim_stop.png')
            stop_icon = stop_icon.resize((17, 17), Image.ANTIALIAS)
            stop_icon = ImageTk.PhotoImage(stop_icon)
            self.menubar.entryconfig(2, image=stop_icon)
            self.menubar.iconPhotoImage = stop_icon

            for gateway in self.canvas.simulation_core.all_gateways:
                reactor.callLater(0.1, gateway.turn_on)
            # yield sleep(0.5)
            for server in self.canvas.simulation_core.all_servers:
                reactor.callLater(0.1, server.turn_on)
            # yield sleep(0.5)   
            for machine in self.canvas.simulation_core.all_machines:
                if machine.type != 'router' or machine.type != 'switch' or machine.type != 'server' or machine.type != 'access_point':
                    reactor.callLater(0.3, machine.turn_on)
                    
            for human in self.canvas.simulation_core.all_humans:
                reactor.callLater(0.3, human.start)
                
            self.dashboard()

    # This method is called when close window button is press. - Rafael Sampaio
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?", icon='warning'):
            if len(self.canvas.simulation_core.all_machines) > 0:
                for machine in self.canvas.simulation_core.all_machines:
                    machine.turn_off()
            log.msg("Info :  - | Closing IoTFogSim Application...")
            reactor.crash()

        else:
            self.canvas.simulation_core.is_running = True
            stop_icon = PIL.Image.open('graphics/icons/iotfogsim_stop.png')
            stop_icon = stop_icon.resize((17, 17), Image.ANTIALIAS)
            stop_icon = ImageTk.PhotoImage(stop_icon)
            self.menubar.entryconfig(2, image=stop_icon)
            self.menubar.iconPhotoImage = stop_icon
            
    
    def dashboard(self):
        window = tkinter.Toplevel()
        tksupport.install(window)
        window.title(
            "IoTFogSim %s - An Distributed Event-Driven Network Simulator" % (version))
        window.geometry("700x900")
        window.resizable(False, False)

        # Setting window icon. - Rafael Sampaio
        window.iconphoto(True, PhotoImage(
            file='graphics/icons/iotfogsim_icon.png'))
