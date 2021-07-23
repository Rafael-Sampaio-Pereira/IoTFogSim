import tkinter
from tkinter import ttk
import pathlib
from tkinter import filedialog
from random import randrange
import PIL
from PIL import Image, ImageTk
from tkinter import PhotoImage
from twisted.internet import tksupport
from config.settings import version
from core.functions import get_all_app_classes_name


def add_new_node_modal_screen(network_layer, node_type):
        window = tkinter.Toplevel()
        tksupport.install(window)
        window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
        window.geometry("400x551")
        window.resizable(False, False)

        # Setting window icon. - Rafael Sampaio
        window.iconphoto(True, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))

        # hearder message - Rafael Sampaio
        create_msg = tkinter.Label(window,text="Create new "+node_type.replace("_"," ")+" at "+network_layer+" layer.")
        create_msg.place(relx="0.1",rely="0.05")

        # New node Name - Rafael Sampaio
        name_label = tkinter.Label(window,text="Name:")
        name_label.place(relx="0.1",rely="0.12")
        input_name = tkinter.Entry(window)
        input_name.place(relx="0.25",rely="0.12")

        # New node position on screen -Rafael Sampaio
        create_msg = tkinter.Label(window,text="Position:")
        create_msg.place(relx="0.1",rely="0.18")
        x = window.winfo_pointerx()
        y = window.winfo_pointery()
        x_label = tkinter.Label(window,text="X")
        x_label.place(relx="0.25",rely="0.18")
        input_x = tkinter.Entry(window)
        input_x.insert(-1, x)
        input_x.place(width="35", relx="0.29", rely="0.18")
        y_label = tkinter.Label(window, text="Y")
        y_label.place(relx="0.45",rely="0.18")
        input_y = tkinter.Entry(window)
        input_y.insert(-1, y)
        input_y.place(width="35", relx="0.49",rely="0.18")

        # input for new node coverage area, deafult is disabled - Rafael Sampaio
        coverage_area_label = tkinter.Label(window,text="Coverage area:")
        coverage_area_label.place(relx="0.1",rely="0.30")
        input_coverage_area = tkinter.Entry(window, state='disabled')
        input_coverage_area.place(width="124", relx="0.35",rely="0.30")

        # controller for radio buttons that enable and disable the coverage are input - Rafael Sampaio 
        radio_button_controller = tkinter.IntVar()

        # function to enable coverage area input - Rafael Sampaio
        def enableCoverage():
            input_coverage_area.configure(state="normal")
            input_coverage_area.update()
        # function to desable coverage area input - Rafael Sampaio
        def disableCoverage():
            input_coverage_area.configure(state="disabled")
            input_coverage_area.update()

        # radio buttons that enable and disable the coverage area input - Rafael Sampaio 
        is_wireless_msg = tkinter.Label(window,text="Is wireless?")
        is_wireless_msg.place(relx="0.1",rely="0.24")
        yes_button = tkinter.Radiobutton(window, text="Yes", variable=radio_button_controller, value="0", command=enableCoverage)
        yes_button.place(relx="0.3",rely="0.24")
        no_button = tkinter.Radiobutton(window, text="No", variable=radio_button_controller, value="1", command=disableCoverage)
        no_button.place(relx="0.45",rely="0.24")

        # geting all apps in 'plications' folder files - Rafael Sampaio 
        all_apps_list = get_all_app_classes_name()

        # combox for apps list - Rafael Sampaio
        all_app_list_label = tkinter.Label(window,text="App:")
        all_app_list_label.place(relx="0.1",rely="0.36")
        cmb_app_list = ttk.Combobox(window, width="21", values=all_apps_list)
        cmb_app_list.place(relx="0.2",rely="0.36")

        # label for the new node icon - Rafael Sampaio
        img = Image.open(str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_server.png')
        img = img.resize((32, 32))
        photo = ImageTk.PhotoImage(img)
        icon_label = tkinter.Label(window, image=photo)
        icon_label.image = photo 
        icon_label.place(relx="0.5",rely="0.42")

        # function to allow the user choose another icon - Rafael Sampaio
        def chooseIconDialog():
            path = str(pathlib.Path.cwd())+'/graphics/icons/'
            filename = filedialog.askopenfilename(initialdir = path, title = "Choose a icon file", filetypes =
            [("png files","*.png")])
            img = Image.open(filename)
            img = img.resize((32, 32))
            photo = ImageTk.PhotoImage(img)
            icon_label.configure(image=photo)
            icon_label.image = photo 
            icon_label.update()

        # button for choose another icon - Rafael Sampaio
        choose_icon_button = ttk.Button(window, text = "Choose another icon",command = chooseIconDialog)
        choose_icon_button.place(relx="0.1",rely="0.42")

        # just a screen separator - Rafael Sampaio
        sep = ttk.Separator(window).place(relx="0.0", rely="0.50", relwidth=1)

        # atributtes only for routers, clients and servers - Rafael Sampaio
        if (node_type == 'router' or node_type == 'client' or node_type == 'server'):
            # New node real ip addr - Rafael Sampaio
            real_ip_label = tkinter.Label(window,text="Real IP:")
            real_ip_label.place(relx="0.1",rely="0.54")
            input_real_ip = tkinter.Entry(window)
            input_real_ip.insert(-1, '127.0.0.1')
            input_real_ip.place(relx="0.25",rely="0.54")


        # atributtes only for routers and servers - Rafael Sampaio
        if (node_type == 'router' or node_type == 'server'):
            # New node port - Rafael Sampaio
            port_label = tkinter.Label(window,text="Port:")
            port_label.place(relx="0.1",rely="0.60")
            input_port = tkinter.Entry(window)
            input_port.insert(-1, str(randrange(8000, 8999)))
            input_port.place(width="50",relx="0.25",rely="0.60")

        # atributtes only for routers - Rafael Sampaio
        if (node_type == 'router'):
            
            def openAPWindow():
                ap_window = tkinter.Toplevel()
                tksupport.install(ap_window)
                ap_window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
                ap_window.geometry("300x200")
                ap_window.resizable(False, False)

                # access point hearder message - Rafael Sampaio
                create_msg = tkinter.Label(ap_window,text="Access Point Info")
                create_msg.place(relx="0.1",rely="0.05")
                
                # input for router access point addr- Rafael Sampaio
                ap_real_ip_label = tkinter.Label(ap_window,text="Real IP:")
                ap_real_ip_label.place(relx="0.1",rely="0.20")
                input_ap_real_ip = tkinter.Entry(ap_window)
                input_ap_real_ip.insert(-1, '127.0.0.1')
                input_ap_real_ip.place(relx="0.25", rely="0.20")

                # input for router access point port - Rafael Sampaio
                ap_port_label = tkinter.Label(ap_window,text="Port:")
                ap_port_label.place(relx="0.1",rely="0.35")
                ap_input_port = tkinter.Entry(ap_window)
                ap_input_port.insert(-1, str(randrange(8000, 8999)))
                ap_input_port.place(width="50",relx="0.25",rely="0.35")

                # access position on screen -Rafael Sampaio
                ap_msg = tkinter.Label(ap_window,text="Position:")
                ap_msg.place(relx="0.1",rely="0.50")
                ap_x_label = tkinter.Label(ap_window,text="X")
                ap_x_label.place(relx="0.25",rely="0.50")
                ap_input_x = tkinter.Entry(ap_window)
                ap_input_x.insert(-1, int(x)+10)
                ap_input_x.place(width="35", relx="0.29", rely="0.50")
                ap_y_label = tkinter.Label(ap_window, text="Y")
                ap_y_label.place(relx="0.45",rely="0.50")
                ap_input_y = tkinter.Entry(ap_window)
                ap_input_y.insert(-1, int(y)+10)
                ap_input_y.place(width="35", relx="0.49",rely="0.50")

                # button to save access point - Rafael Sampaio
                save_ap_button = ttk.Button(ap_window, text = "Save", command = None)
                save_ap_button.place(relx="0.35",rely="0.70")

            # button to open a modal to create access point - Rafael Sampaio
            ap_button = ttk.Button(window, text = "Add Access Point", command = openAPWindow)
            ap_button.place(relx="0.1",rely="0.66")
        
        # button to save the new node - Rafael Sampaio
        save_node_button = ttk.Button(window, text = "Save", command = None)
        save_node_button.place(relx="0.4",rely="0.90")