import tkinter
from tkinter import PhotoImage
from twisted.internet import tksupport
from twisted.python import log
from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint
from scinetsim.standarddevice import Router
from scinetsim.standarddevice import WSNSensorNode
from scinetsim.standarddevice import WSNRepeaterNode
from scinetsim.standarddevice import WSNSinkNode
from scinetsim.standarddevice import WirelessSensorNetwork
from scinetsim.standarddevice import WirelessComputer

from scinetsim.ScrollableScreen import ScrollableScreen
from scinetsim.simulationcore import SimulationCore
import json
import os
from tkinter import ttk
from tkinter import messagebox
from config.settings import version

from scinetsim.functions import configure_logger

import time

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

			simulation_core.project_name = selected_project_name

			# Configuring log - Rafael Sampaio
			log_path = "projects/"+selected_project_name+"/"
			configure_logger(log_path, selected_project_name)

			simulation_core.create_simulation_canvas()
			load_nodes(selected_project_name, simulation_core)
			#load_connections(selected_project_name, simulation_core)

			window.destroy()
			window.update()

	def creat_project(window,new_project_name, simulation_core):
		try:
			os.makedirs("projects/%s"%(new_project_name))

			# Configuring log - Rafael Sampaio
			log_path = "projects/"+new_project_name+"/"
			configure_logger(log_path, new_project_name)

			simulation_core.project_name = new_project_name

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

	# Interval between nodes creation and nodes start(run)- Rafael Sampaio
	interval=0.5

	with open('projects/'+project_name+'/nodes.js', 'r') as nodes_file:
		data = json.loads(nodes_file.read())
		
		if data:
    		
			################## LOADING FOG DEVICES - Rafael Sampaio ##################
			

			for router in data['fog']['routers']:
    				
				log.msg("Creating router ...")
				rt = Router(simulation_core, router['port'], router['real_ip'], router['simulation_ip'], router['id'],router['name'], router['icon'], router['is_wireless'], router['x'], router['y'], router['application'], router['coverage_area_radius'])
				simulation_core.allNodes.add(rt)
				time.sleep(interval)
				rt.run()

				for access_point in router['access_points']:
						
					log.msg("Creating AccessPoint station ...")

					ap = AccessPoint(simulation_core, rt, access_point['id'], access_point['TBTT'], access_point['SSID'], access_point['WPA2_password'], access_point['icon'], access_point['is_wireless'], access_point['x'], access_point['y'], access_point['application'], access_point['coverage_area_radius'])
					simulation_core.allNodes.add(ap)
					time.sleep(interval)
					ap.run()


			for computer in data['fog']['wireless_computers']:
    					
				comp = WirelessComputer(simulation_core, computer['id'], computer['name'], computer['icon'], computer['is_wireless'], computer['x'], computer['y'], computer['application'], computer['coverage_area_radius'])
				simulation_core.allNodes.add(comp) 
				time.sleep(interval)
				comp.run()

			
			for server in data['fog']['servers']:
								
				sr = StandardServerDevice(simulation_core, server['port'], server['real_ip'], server['simulation_ip'], server['id'], server['name'], server['icon'], server['is_wireless'], server['x'], server['y'], server['application'], server['coverage_area_radius'])
				simulation_core.allNodes.add(sr)
				time.sleep(interval)
				sr.run()
			
			
			
			for client in data['fog']['clients']:
								
				cl = StandardClientDevice(simulation_core, client['real_ip'], client['simulation_ip'], client['id'], client['name'], client['icon'], client['is_wireless'], client['x'], client['y'], client['application'], client['coverage_area_radius'])
				simulation_core.allNodes.add(cl)
				time.sleep(interval)
				cl.run()
					

			for wsn in data['fog']['wireless_sensor_networks']:

				sink_cont = 0
				repeater_cont = 0
				sensor_cont = 0
				WSN_network_group = WirelessSensorNetwork(simulation_core, wsn['wireless_standard'], wsn['network_layer_protocol'])

				for sink_node in wsn['sink_nodes']:
					sink_cont += 1
					sk_node = WSNSinkNode(simulation_core, sink_cont, sink_node['name'], sink_node['icon'], sink_node['is_wireless'], sink_node['x'], sink_node['y'], sink_node['application'], sink_node['coverage_area_radius'], WSN_network_group)
					WSN_network_group.sink_list.add(sk_node)
					time.sleep(interval)

				for sensor_node in wsn['sensor_nodes']:
					sensor_cont += 1
					sr_node = WSNSensorNode(simulation_core, sensor_cont, sensor_node['name'], sensor_node['icon'], sensor_node['is_wireless'], sensor_node['x'], sensor_node['y'], sensor_node['application'], sensor_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.sensors_list.add(sr_node)
					time.sleep(interval)

				for repeater_node in wsn['repeater_nodes']:
					repeater_cont += 1
					rpt_node = WSNRepeaterNode(simulation_core, repeater_cont, repeater_node['name'], repeater_node['icon'], repeater_node['is_wireless'], repeater_node['x'], repeater_node['y'], repeater_node['application'], repeater_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.repeater_list.add(rpt_node)
					time.sleep(interval)


				# The devices needs to be started in separated function to allow the correct load of the nearby devices list - Rafael Sampaio
				for deivce in WSN_network_group.sink_list:
					deivce.run()

				for deivce in WSN_network_group.sensors_list:
					deivce.run()

				for deivce in WSN_network_group.repeater_list:
					deivce.run()



			
			################## LOADING CLOUD DEVICES - Rafael Sampaio ##################
			for router in data['cloud']['routers']:
    				

				log.msg("Creating router ...")
				rt = Router(simulation_core, router['port'], router['real_ip'], router['simulation_ip'], router['id'],router['name'], router['icon'], router['is_wireless'], router['x'], router['y'], router['application'], router['coverage_area_radius'])
				simulation_core.allNodes.add(rt)
				time.sleep(interval)
				rt.run()

				for access_point in router['access_points']:
						
					log.msg("Creating AccessPoint station ...")

					ap = AccessPoint(simulation_core, rt, access_point['id'], access_point['TBTT'], access_point['SSID'], access_point['WPA2_password'], access_point['icon'], access_point['is_wireless'], access_point['x'], access_point['y'], access_point['application'], access_point['coverage_area_radius'])
					simulation_core.allNodes.add(ap)
					time.sleep(interval)
					ap.run()
			
			for server in data['cloud']['servers']:
								
				sr = StandardServerDevice(simulation_core, server['port'], server['real_ip'], server['simulation_ip'], server['id'], server['name'], server['icon'], server['is_wireless'], server['x'], server['y'], server['application'], server['coverage_area_radius'])
				simulation_core.allNodes.add(sr)
				time.sleep(interval)
				sr.run()

			for client in data['cloud']['clients']:
								
				cl = StandardClientDevice(simulation_core, client['real_ip'], client['simulation_ip'], client['id'], client['name'], client['icon'], client['is_wireless'], client['x'], client['y'], client['application'], client['coverage_area_radius'])
				simulation_core.allNodes.add(cl)
				time.sleep(interval)
				cl.run()
					

			for wsn in data['cloud']['wireless_sensor_networks']:

				sink_cont = 0
				repeater_cont = 0
				sensor_cont = 0
				WSN_network_group = WirelessSensorNetwork(simulation_core, wsn['wireless_standard'], wsn['network_layer_protocol'])

				for sink_node in wsn['sink_nodes']:
					sink_cont += 1
					sk_node = WSNSinkNode(simulation_core, sink_cont, sink_node['name'], sink_node['icon'], sink_node['is_wireless'], sink_node['x'], sink_node['y'], sink_node['application'], sink_node['coverage_area_radius'], WSN_network_group)
					WSN_network_group.sink_list.add(sk_node)
					time.sleep(interval)

				for sensor_node in wsn['sensor_nodes']:
					sensor_cont += 1
					sr_node = WSNSensorNode(simulation_core, sensor_cont, sensor_node['name'], sensor_node['icon'], sensor_node['is_wireless'], sensor_node['x'], sensor_node['y'], sensor_node['application'], sensor_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.sensors_list.add(sr_node)
					time.sleep(interval)

				for repeater_node in wsn['repeater_nodes']:
					repeater_cont += 1
					rpt_node = WSNRepeaterNode(simulation_core, repeater_cont, repeater_node['name'], repeater_node['icon'], repeater_node['is_wireless'], repeater_node['x'], repeater_node['y'], repeater_node['application'], repeater_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.repeater_list.add(rpt_node)
					time.sleep(interval)

				# The devices needs to be started in separated function to allow the correct load of the nearby devices list - Rafael Sampaio
				for deivce in WSN_network_group.sink_list:
					deivce.run()

				for deivce in WSN_network_group.sensors_list:
					deivce.run()

				for deivce in WSN_network_group.repeater_list:
					deivce.run()

			
			for computer in data['cloud']['wireless_computers']:
					
				comp = WirelessComputer(simulation_core, computer['id'], computer['name'], computer['icon'], computer['is_wireless'], computer['x'], computer['y'], computer['application'], computer['coverage_area_radius'])
				simulation_core.allNodes.add(comp) 
				time.sleep(interval)
				comp.run()


			################## LOADING IOT DEVICES - Rafael Sampaio ##################
			for router in data['iot']['routers']:
    				

				log.msg("Creating router ...")
				rt = Router(simulation_core, router['port'], router['real_ip'], router['simulation_ip'], router['id'],router['name'], router['icon'], router['is_wireless'], router['x'], router['y'], router['application'], router['coverage_area_radius'])
				simulation_core.allNodes.add(rt)
				time.sleep(interval)
				rt.run()

				for access_point in router['access_points']:
						
					log.msg("Creating AccessPoint station ...")

					ap = AccessPoint(simulation_core, rt, access_point['id'], access_point['TBTT'], access_point['SSID'], access_point['WPA2_password'], access_point['icon'], access_point['is_wireless'], access_point['x'], access_point['y'], access_point['application'], access_point['coverage_area_radius'])
					simulation_core.allNodes.add(ap)
					time.sleep(interval)
					ap.run()
			
			for server in data['iot']['servers']:
								
				sr = StandardServerDevice(simulation_core, server['port'], server['real_ip'], server['simulation_ip'], server['id'], server['name'], server['icon'], server['is_wireless'], server['x'], server['y'], server['application'], server['coverage_area_radius'])
				simulation_core.allNodes.add(sr)
				time.sleep(interval)
				sr.run()

			for client in data['iot']['clients']:
								
				cl = StandardClientDevice(simulation_core, client['real_ip'], client['simulation_ip'], client['id'], client['name'], client['icon'], client['is_wireless'], client['x'], client['y'], client['application'], client['coverage_area_radius'])
				simulation_core.allNodes.add(cl)
				time.sleep(interval)
				cl.run()
					

			for wsn in data['iot']['wireless_sensor_networks']:

				sink_cont = 0
				repeater_cont = 0
				sensor_cont = 0
				WSN_network_group = WirelessSensorNetwork(simulation_core, wsn['wireless_standard'], wsn['network_layer_protocol'])

				for sink_node in wsn['sink_nodes']:
					sink_cont += 1
					sk_node = WSNSinkNode(simulation_core, sink_cont, sink_node['name'], sink_node['icon'], sink_node['is_wireless'], sink_node['x'], sink_node['y'], sink_node['application'], sink_node['coverage_area_radius'], WSN_network_group)
					WSN_network_group.sink_list.add(sk_node)
					time.sleep(interval)

				for sensor_node in wsn['sensor_nodes']:
					sensor_cont += 1
					sr_node = WSNSensorNode(simulation_core, sensor_cont, sensor_node['name'], sensor_node['icon'], sensor_node['is_wireless'], sensor_node['x'], sensor_node['y'], sensor_node['application'], sensor_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.sensors_list.add(sr_node)
					time.sleep(interval)

				for repeater_node in wsn['repeater_nodes']:
					repeater_cont += 1
					rpt_node = WSNRepeaterNode(simulation_core, repeater_cont, repeater_node['name'], repeater_node['icon'], repeater_node['is_wireless'], repeater_node['x'], repeater_node['y'], repeater_node['application'], repeater_node['coverage_area_radius'],WSN_network_group)
					WSN_network_group.repeater_list.add(rpt_node)
					time.sleep(interval)
    				

				# The devices needs to be started in separated function to allow the correct load of the nearby devices list - Rafael Sampaio
				for deivce in WSN_network_group.sink_list:
					deivce.run()

				for deivce in WSN_network_group.sensors_list:
					deivce.run()
				
				for deivce in WSN_network_group.repeater_list:
					deivce.run()


			
			for computer in data['iot']['wireless_computers']:
					
				comp = WirelessComputer(simulation_core, computer['id'], computer['name'], computer['icon'], computer['is_wireless'], computer['x'], computer['y'], computer['application'], computer['coverage_area_radius'])
				simulation_core.allNodes.add(comp) 
				time.sleep(interval)
				comp.run()


				



				
