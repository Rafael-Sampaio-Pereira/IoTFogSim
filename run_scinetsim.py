from twisted.internet import reactor
from twisted.python import log
import sys
import tkinter
from tkinter import PhotoImage
from scinetsim.standarddevice import StandardServerDevice
from scinetsim.standarddevice import StandardClientDevice
from scinetsim.standarddevice import AccessPoint
from scinetsim.standarddevice import Connection
import PIL
from PIL import ImageTk, Image
import random

from scinetsim.configurations import config

import json



def main():
	canvas = config()

	allWirelessConnections = []
	allConnections = []

	allFogNodes = []
	allCloudNodes = []
	allAccessPoints= []
	allRoutersNodes = []
	allIoTNodes = []


	with open('nodes.js') as nodes_file:
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

				

			


	#server = StandardServerDevice(canvas)
	#server.run()




	#client = StandardClientDevice(canvas)
	#client.run()
	#ap = AccessPoint(canvas)

	#con1 = Connection(canvas,ap,client)





if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()