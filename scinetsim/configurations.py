import tkinter
from tkinter import PhotoImage
from twisted.internet import tksupport
from twisted.python import log
from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint
from scinetsim.standarddevice import Connection
from scinetsim.ScrollableScreen import ScrollableScreen
import json
from config.settings import version
import os

from tkinter import ttk
from tkinter import messagebox

def config():
	initialization_screen()
	
	


def initialization_screen():
	window = tkinter.Toplevel()
	tksupport.install(window)
	window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
	window.geometry("400x400")
	window.resizable(False, False)

	# Getting all projects folders name from the directory 'projects' and saving it on a list - Rafael Sampaio
	projects_list = [f.name for f in os.scandir("projects") if f.is_dir() ]

	def open_project():
	    selected_project_name = cmb_projects_list.get()
	    messagebox.showinfo("IoTFogSim - %s"%(selected_project_name), "You're begin to start the %s simulation project. Just click the 'Ok' button." %(selected_project_name))
	    
	    canvas = create_simulation_canvas()
	    load_nodes(canvas,selected_project_name)

	    window.destroy()

	cmb_projects_list = ttk.Combobox(window, width="10", values=projects_list)
	cmb_projects_list.place(relx="0.1",rely="0.1")

	label_one = tkinter.Label(window,text="Select a project to open:")
	label_one.place(relx="0.1",rely="0.04")

	btn_open = ttk.Button(window, text="Open Project",command=open_project)
	btn_open.place(relx="0.5",rely="0.1")

	sep = ttk.Separator(window).place(relx="0.0", rely="0.2", relwidth=1)

	label_two = tkinter.Label(window,text="Or create a new one and start.")
	label_two.place(relx="0.1",rely="0.23")

	label_three = tkinter.Label(window,text="Project name:")
	label_three.place(relx="0.1",rely="0.3")

	input_new_project_name = tkinter.Entry(window)
	input_new_project_name.place(relx="0.4",rely="0.3")

	btn_new = ttk.Button(window, text="Create new project and start it",command=None)
	btn_new.place(relx="0.2",rely="0.4")

	#root.mainloop()
















def create_simulation_canvas():
	
	# These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
	window = tkinter.Toplevel()
	tksupport.install(window)

	# Main window size and positions settings. - Rafael Sampaio
	w_heigth = 600
	w_width = 800
	w_top_padding = 80
	w_letf_padding = 100
	window.geometry(str(w_width)+"x"+str(w_heigth)+"+"+str(w_letf_padding)+"+"+str(w_top_padding))

	# Setting window icon. - Rafael Sampaio
	window.tk.call('wm', 'iconphoto', window._w, PhotoImage(master=window,file='graphics/icons/iotfogsim_icon.png'))
	
	# Setting window top text. - Rafael Sampaio
	window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
	
	# Simulation area on screen. - Rafael Sampaio
	simulation_screen = ScrollableScreen(window)
	simulation_screen.pack(fill="both", expand=True)
	canvas = simulation_screen.getCanvas()

	return canvas


def load_nodes(canvas, project_name):

	allWirelessConnections = []
	allConnections = []

	allFogNodes = []
	allCloudNodes = []
	allAccessPoints= []
	allRoutersNodes = []
	allIoTNodes = []


	with open('projects/'+project_name+'/nodes.js') as nodes_file:
		data = json.load(nodes_file)
		
		for fog_node in data['fog_nodes']:
			
			log.msg("Creating fog node ...")
			fog = None
			
			if(fog_node['type'] == 'server'):
				fog = StandardServerDevice(canvas, fog_node['real_ip'], fog_node['simulation_ip'], fog_node['name'], fog_node['icon'], fog_node['is_wireless'], fog_node['x'], fog_node['y'])
				allFogNodes.append(fog)
				fog.run()
				
			elif(fog_node['type'] == 'client'):
				fog = StandardClientDevice(canvas, fog_node['real_ip'], fog_node['simulation_ip'], fog_node['name'], fog_node['icon'], fog_node['is_wireless'], fog_node['x'], fog_node['y'])
				allFogNodes.append(fog)
				fog.run()
				
			else:
				log.msg("Error: Type not found.")

		for cloud_node in data['cloud_nodes']:
			
			log.msg("Creating cloud node ...")
			fog = None
			
			if(cloud_node['type'] == 'server'):
				cloud = StandardServerDevice(canvas, cloud_node['real_ip'], cloud_node['simulation_ip'], cloud_node['name'], cloud_node['icon'], cloud_node['is_wireless'], cloud_node['x'], cloud_node['y'])
				allCloudNodes.append(cloud)
				cloud.run()
				
			elif(cloud_node['type'] == 'client'):
				cloud = StandardClientDevice(canvas, cloud_node['real_ip'], cloud_node['simulation_ip'], cloud_node['name'], cloud_node['icon'], cloud_node['is_wireless'], cloud_node['x'], cloud_node['y'])
				allCloudNodes.append(cloud)
				cloud.run()
				
			else:
				log.msg("Error: Type not found.")

		for iot_node in data['iot_nodes']:
			
			log.msg("Creating iot node ...")
			iot = None
			
			if(iot_node['type'] == 'server'):
				iot = StandardServerDevice(canvas, iot_node['real_ip'], iot_node['simulation_ip'], iot_node['name'], iot_node['icon'], iot_node['is_wireless'], iot_node['x'], iot_node['y'])
				allIoTNodes.append(iot)
				iot.run()
				
			elif(iot_node['type'] == 'client'):
				iot = StandardClientDevice(canvas, iot_node['real_ip'], iot_node['simulation_ip'], iot_node['name'], iot_node['icon'], iot_node['is_wireless'], iot_node['x'], iot_node['y'])
				allIoTNodes.append(iot)
				iot.run()
				
			else:
				log.msg("Error: Type not found.")


		for access_point in data['access_points']:
			
			log.msg("Creating iot node ...")
			
			ap = AccessPoint(canvas, access_point['simulation_ip'], access_point['TBTT'], access_point['SSID'], access_point['WPA2_password'], access_point['icon'], access_point['is_wireless'], access_point['x'], access_point['y'])
			allAccessPoints.append(iot)