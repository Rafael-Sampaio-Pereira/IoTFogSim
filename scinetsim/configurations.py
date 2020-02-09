import tkinter
from tkinter import PhotoImage
from twisted.internet import tksupport
from twisted.python import log
from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint
from scinetsim.standarddevice import Router
from scinetsim.standarddevice import Connection
from scinetsim.ScrollableScreen import ScrollableScreen
from scinetsim.simulationcore import SimulationCore
import json
import os
from tkinter import ttk
from tkinter import messagebox
from config.settings import version

def config():
	# para que uma aplicação com tkinter possa usar varias janelas é preciso uma instancia de tkinter.Tk()
	# que será o pai. As janelas(filhas) devem ser cirdas com tkinter.Toplevel() - Rafael Sampaio
	root = tkinter.Tk()
	# escondendo a instancia vazia de tk() para evitar a exibição desnecessária - Rafael Sampaio
	root.withdraw()

	simulation_core = SimulationCore()

	initialization_screen(simulation_core)
	
	
def initialization_screen(simulation_core):
	window = tkinter.Toplevel()
	tksupport.install(window)
	window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
	window.geometry("400x551")
	window.resizable(False, False)

	# Setting window icon. - Rafael Sampaio
	window.iconphoto(True, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))
	
	# returns a list with all the subdirectoys in a folder -  Rafael Sampaio
	def load_projects(directory):
		return [f.name for f in os.scandir(directory) if f.is_dir() ]

	def open_project(window, simulation_core):
	    selected_project_name = cmb_projects_list.get()
	    messagebox.showinfo("IoTFogSim - %s"%(selected_project_name), "You're begin to start the %s simulation project. Just click the 'Ok' button." %(selected_project_name))
	    
	    simulation_core.create_simulation_canvas()
	    load_nodes(selected_project_name, simulation_core)
	    load_connections(selected_project_name, simulation_core)

	    window.destroy()
	    window.update()

	def creat_project(window,new_project_name, simulation_core):
		try:
			os.makedirs("projects/%s"%(new_project_name))

			# creating the nodes.js file into the project directory - Rafael Sampaio
			nodes_file = "projects/%s/nodes.js"%(new_project_name)
			if not os.path.exists(nodes_file):
				with open(nodes_file, 'w') as file:
					print("{}", file=file)

			simulation_core.create_simulation_canvas()
			load_nodes(new_project_name, simulation_core)
			
			window.destroy()
			window.update()

		except FileExistsError:
		    # if the directory already exists - Rafael Sampaio
		    messagebox.showerror("IoTFogSim - Error while create project", "The project %s already exists!"%(new_project_name))


	# Getting all projects folders name from the directory 'projects' and saving it on a list - Rafael Sampaio
	projects_list = load_projects("projects")

	#configure backgroud image - Rafael Sampaio
	bg_image = PhotoImage(file ="graphics/images/background1.png")
	x = tkinter.Label(window,image = bg_image)
	x.place(relx="0.0",rely="0.0")
	x.img = bg_image

	cmb_projects_list = ttk.Combobox(window, width="10", values=projects_list)
	cmb_projects_list.place(relx="0.1",rely="0.1")

	label_one = tkinter.Label(window,text="Select a project to open:")
	label_one.place(relx="0.1",rely="0.04")

	btn_open = ttk.Button(window, text="Open Project",command=lambda:open_project(window,simulation_core))
	btn_open.place(relx="0.5",rely="0.1")

	sep = ttk.Separator(window).place(relx="0.0", rely="0.2", relwidth=1)

	label_two = tkinter.Label(window,text="Or create a new one and start.")
	label_two.place(relx="0.1",rely="0.23")

	label_three = tkinter.Label(window,text="Project name:")
	label_three.place(relx="0.1",rely="0.3")

	input_new_project_name = tkinter.Entry(window)
	input_new_project_name.place(relx="0.4",rely="0.3")

	btn_new = ttk.Button(window, text="Create new project and start it",command = lambda: creat_project(window,input_new_project_name.get(), simulation_core))
	btn_new.place(relx="0.2",rely="0.4")





def load_nodes(project_name, simulation_core):

	allWirelessConnections = []
	allConnections = []

	with open('projects/'+project_name+'/nodes.js') as nodes_file:
		data = json.load(nodes_file)
		
		if data:
    		
			for router in data['routers']:

				log.msg("Creating router ...")
				#print(router['icon'])
				rt = Router(simulation_core, router['port'], router['real_ip'], router['simulation_ip'], router['id'],router['name'], router['icon'], router['is_wireless'], router['x'], router['y'], router['application'])
				simulation_core.appendRouterNodes(rt)
				rt.run()

			for access_point in data['access_points']:
    				
				log.msg("Creating AccessPoint station ...")
				
				ap = AccessPoint(simulation_core, access_point['simulation_ip'], access_point['id'], access_point['TBTT'], access_point['SSID'], access_point['WPA2_password'], access_point['icon'], access_point['is_wireless'], access_point['x'], access_point['y'])
				simulation_core.appendAccessPointNode(iot)
		
			for fog_node in data['fog_nodes']:
				
				log.msg("Creating fog node ...")
				fog = None
				
				if(fog_node['type'] == 'server'):
					fog = StandardServerDevice(simulation_core, fog_node['real_ip'], fog_node['simulation_ip'], fog_node['id'], fog_node['name'], fog_node['icon'], fog_node['is_wireless'], fog_node['x'], fog_node['y'], fog_node['application'])
					simulation_core.appendFogNodes(fog)
					fog.run()
					
				elif(fog_node['type'] == 'client'):
					fog = StandardClientDevice(simulation_core, fog_node['real_ip'], fog_node['simulation_ip'], fog_node['id'],fog_node['name'], fog_node['icon'], fog_node['is_wireless'], fog_node['x'], fog_node['y'], fog_node['application'])
					simulation_core.appendFogNodes(fog)
					fog.run()
					
				else:
					log.msg("Error: Type not found.")

			for cloud_node in data['cloud_nodes']:
				
				log.msg("Creating cloud node ...")
				fog = None
				
				if(cloud_node['type'] == 'server'):
					cloud = StandardServerDevice(simulation_core, cloud_node['real_ip'], cloud_node['simulation_ip'], cloud_node['id'],cloud_node['name'], cloud_node['icon'], cloud_node['is_wireless'], cloud_node['x'], cloud_node['y'], cloud_node['application'])
					simulation_core.appendCloudNodes(cloud)
					cloud.run()
					
				elif(cloud_node['type'] == 'client'):
					cloud = StandardClientDevice(simulation_core, cloud_node['real_ip'], cloud_node['simulation_ip'], cloud_node['id'],cloud_node['name'], cloud_node['icon'], cloud_node['is_wireless'], cloud_node['x'], cloud_node['y'], cloud_node['application'])
					simulation_core.appendCloudNodes(cloud)
					cloud.run()
					
				else:
					log.msg("Error: Type not found.")

			for iot_node in data['iot_nodes']:
				
				log.msg("Creating iot node ...")
				iot = None
				
				if(iot_node['type'] == 'server'):
					iot = StandardServerDevice(simulation_core, iot_node['real_ip'], iot_node['simulation_ip'], iot_node['id'],iot_node['name'], iot_node['icon'], iot_node['is_wireless'], iot_node['x'], iot_node['y'], iot_node['application'])
					simulation_core.appendIoTNodes(iot)
					iot.run()
					
				elif(iot_node['type'] == 'client'):
					iot = StandardClientDevice(simulation_core, iot_node['real_ip'], iot_node['simulation_ip'],  iot_node['id'],iot_node['name'], iot_node['icon'], iot_node['is_wireless'], iot_node['x'], iot_node['y'], iot_node['application'])
					simulation_core.appendIoTNodes(iot)
					iot.run()
					
				else:
					log.msg("Error: Type not found.")


			
				


def load_connections(project_name, simulation_core):


	with open('projects/'+project_name+'/connections.js') as connections_file:
		data = json.load(connections_file)
		
		if data:
			for connection in data['connections']:
				
				log.msg("Creating connections ...")

				con = Connection(simulation_core, connection['id_device_1'], connection['id_device_2'])

				simulation_core.appendConnections(con)