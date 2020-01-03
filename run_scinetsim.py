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
	allAccessPointsNodes = []
	allRoutersNodes = []


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

			


	#server = StandardServerDevice(canvas)
	#server.run()




	#client = StandardClientDevice(canvas)
	#client.run()
	ap = AccessPoint(canvas)

	#con1 = Connection(canvas,ap,client)





if __name__ == '__main__':
    log.startLogging(sys.stdout)
    main()
    reactor.run()