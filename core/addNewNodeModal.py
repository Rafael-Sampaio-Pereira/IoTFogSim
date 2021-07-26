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
from core.standarddevice import StandardServerDevice
from core.standarddevice import StandardClientDevice
from core.standarddevice import AccessPoint
from core.standarddevice import Router
from core.standarddevice import WSNSensorNode
from core.standarddevice import WSNRepeaterNode
from core.standarddevice import WSNSinkNode
from core.standarddevice import WirelessSensorNetwork
from core.standarddevice import WirelessComputer
from core.iconsRegister import getIconName
import os

def add_new_node_modal_screen(simulation_core, network_layer, node_type):
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
        input_coverage_area = tkinter.Entry(window)
        input_coverage_area.insert(-1, 0)
        input_coverage_area.configure(state='disabled')
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
        yes_button = tkinter.Radiobutton(window, text="Yes", variable=radio_button_controller, value="1", command=enableCoverage)
        yes_button.place(relx="0.3",rely="0.24")
        no_button = tkinter.Radiobutton(window, text="No", variable=radio_button_controller, value="0", command=disableCoverage)
        no_button.place(relx="0.45",rely="0.24")

        # geting all apps in 'plications' folder files - Rafael Sampaio 
        all_apps_list = get_all_app_classes_name()

        # combox for apps list - Rafael Sampaio
        all_app_list_label = tkinter.Label(window,text="App:")
        all_app_list_label.place(relx="0.1",rely="0.36")
        cmb_app_list = ttk.Combobox(window, width="21", values=all_apps_list)
        cmb_app_list.place(relx="0.2",rely="0.36")

        filename = filename = str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_server.png'

        if node_type == 'wireless_computer':
            filename = str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_notebook.png'
        elif node_type == 'router':
            filename = str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_router.png'
        elif node_type == 'server':
            filename = str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_server.png'
        elif node_type == 'client':
            filename = str(pathlib.Path.cwd())+'/graphics/icons/iotfogsim_client.png'


        simulation_core.temp_node_icon_path = filename
        simulation_core.temp_new_ap_node = None

        # label for the new node icon - Rafael Sampaio
        img = Image.open(filename)
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
            simulation_core.temp_node_icon_path = filename
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
                ap_window.geometry("300x300")
                ap_window.resizable(False, False)

                # access point hearder message - Rafael Sampaio
                create_msg = tkinter.Label(ap_window,text="Access Point Info")
                create_msg.place(relx="0.1",rely="0.05")
                
                # input for router access point addr- Rafael Sampaio
                ap_real_ip_label = tkinter.Label(ap_window,text="Real IP:")
                ap_real_ip_label.place(relx="0.1",rely="0.15")
                input_ap_real_ip = tkinter.Entry(ap_window)
                input_ap_real_ip.insert(-1, '127.0.0.1')
                input_ap_real_ip.place(relx="0.25", rely="0.15")

                # input for router access point port - Rafael Sampaio
                ap_port_label = tkinter.Label(ap_window,text="Port:")
                ap_port_label.place(relx="0.1",rely="0.25")
                ap_input_port = tkinter.Entry(ap_window)
                ap_input_port.insert(-1, str(randrange(8000, 8999)))
                ap_input_port.place(width="50",relx="0.25",rely="0.25")

                # access position on screen -Rafael Sampaio
                ap_msg = tkinter.Label(ap_window,text="Position:")
                ap_msg.place(relx="0.1",rely="0.35")
                ap_x_label = tkinter.Label(ap_window,text="X")
                ap_x_label.place(relx="0.25",rely="0.35")
                ap_input_x = tkinter.Entry(ap_window)
                ap_input_x.insert(-1, int(x)+100)
                ap_input_x.place(width="35", relx="0.29", rely="0.35")
                ap_y_label = tkinter.Label(ap_window, text="Y")
                ap_y_label.place(relx="0.45",rely="0.35")
                ap_input_y = tkinter.Entry(ap_window)
                ap_input_y.insert(-1, int(y)+100)
                ap_input_y.place(width="35", relx="0.49",rely="0.35")

                # input for access point addr TBTT- Rafael Sampaio
                ap_tbtt_label = tkinter.Label(ap_window,text="TBTT:")
                ap_tbtt_label.place(relx="0.1",rely="0.45")
                input_ap_tbtt = tkinter.Entry(ap_window)
                input_ap_tbtt.insert(-1, '0.1024')
                input_ap_tbtt.place(relx="0.25", rely="0.45")

                # input for access point addr ssid- Rafael Sampaio
                ap_ssid_label = tkinter.Label(ap_window,text="SSID:")
                ap_ssid_label.place(relx="0.1",rely="0.55")
                input_ap_ssid = tkinter.Entry(ap_window)
                input_ap_ssid.insert(-1, 'Privated Network')
                input_ap_ssid.place(relx="0.25", rely="0.55")

                # input for access point addr wpa2- Rafael Sampaio
                ap_wpa2_label = tkinter.Label(ap_window,text="WPA2:")
                ap_wpa2_label.place(relx="0.1",rely="0.65")
                input_ap_wpa2 = tkinter.Entry(ap_window)
                input_ap_wpa2.insert(-1, '123@iotFogSim2021')
                input_ap_wpa2.place(relx="0.25", rely="0.65")


                # input for new node coverage area, deafult is disabled - Rafael Sampaio
                ap_coverage_area_label = tkinter.Label(ap_window,text="Coverage area:")
                ap_coverage_area_label.place(relx="0.1",rely="0.75")
                input_ap_coverage_area = tkinter.Entry(ap_window)
                input_ap_coverage_area.insert(-1, 200)
                input_ap_coverage_area.place(width="124", relx="0.35",rely="0.75")

                def save_ap():
                    simulation_core.temp_new_ap_node = {
                        'port': int(ap_input_port.get()),
                        'real_ip': input_ap_real_ip.get(),
                        'pos_x': int(ap_input_x.get()),
                        'pos_y': int(ap_input_y.get()),
                        'tbtt': float(input_ap_tbtt.get()),
                        'ssid': input_ap_ssid.get(),
                        'wpa2_password': input_ap_wpa2.get(),
                        'coverage_area_radius': int(input_ap_coverage_area.get())
                    }
                
                    ap_window.destroy()
                    ap_window.update()

                # button to save access point - Rafael Sampaio
                save_ap_button = ttk.Button(ap_window, text = "Save", command = save_ap)
                save_ap_button.place(relx="0.35",rely="0.85")

            # button to open a modal to create access point - Rafael Sampaio
            ap_button = ttk.Button(window, text = "Add Access Point", command = openAPWindow)
            ap_button.place(relx="0.1",rely="0.66")
        
        


        def save():
            name = input_name.get()
            icon_file_name = os.path.basename(simulation_core.temp_node_icon_path)
            icon_name = getIconName(icon_file_name)
            is_wireless = None
            pos_x = input_x.get()
            pos_y = input_y.get()
            if radio_button_controller.get() == 1:
                is_wireless = True
            elif radio_button_controller.get() == 0:
                is_wireless = False
            app = 'applications.'+cmb_app_list.get()
            covarage = input_coverage_area.get()

            # atributtes only for routers, clients and servers - Rafael Sampaio
            if (node_type == 'router' or node_type == 'client' or node_type == 'server'):
                real_ip = input_real_ip.get()

            # atributtes only for routers and servers - Rafael Sampaio
            if (node_type == 'router'or node_type == 'server'):    
                port = input_port.get()

            if (node_type == 'wireless_computer'):

                is_wireless = True

                comp = WirelessComputer(simulation_core,
                name,
                icon_name,
                is_wireless,
                int(pos_x),
                int(pos_y),
                app, 
                int(covarage))
                simulation_core.allNodes.append(comp)
                # comp.run()

            if (node_type == 'server'):
    
                serv = StandardServerDevice(simulation_core,
                int(port),
                real_ip,
                name,
                icon_name,
                is_wireless,
                int(pos_x),
                int(pos_y),
                app, 
                int(covarage))
                simulation_core.allNodes.append(serv)
                # serv.run()

            if (node_type == 'client'):
        
                clt = StandardClientDevice(simulation_core,
                real_ip,
                name,
                icon_name,
                is_wireless,
                int(pos_x),
                int(pos_y),
                app, 
                int(covarage))
                simulation_core.allNodes.append(clt)

            if (node_type == 'router'):

                is_wireless = False
                rtr = Router(simulation_core,
                int(port),
                real_ip,
                name,
                icon_name,
                is_wireless,
                int(pos_x),
                int(pos_y),
                app, 
                int(covarage))
                simulation_core.allNodes.append(rtr)

                if (simulation_core.temp_new_ap_node):
                    application = "applications.accesspointapp.AccessPointApp"
                    icon = "ap_icon"
                    is_wireless = True
                    ap = AccessPoint(simulation_core, 
                    rtr, 
                    simulation_core.temp_new_ap_node['tbtt'], 
                    simulation_core.temp_new_ap_node['ssid'], 
                    simulation_core.temp_new_ap_node['wpa2_password'], 
                    icon, 
                    is_wireless, 
                    simulation_core.temp_new_ap_node['pos_x'], 
                    simulation_core.temp_new_ap_node['pos_y'], 
                    application, 
                    simulation_core.temp_new_ap_node['coverage_area_radius'])
                    ap.gateway_addr = rtr.addr
                    ap.gateway_port = rtr.port
                    simulation_core.allNodes.append(ap)

            window.destroy()
            window.update()

        
        # button to save the new node - Rafael Sampaio
        save_node_button = ttk.Button(window, text = "Save", command = save)
        save_node_button.place(relx="0.4",rely="0.90")