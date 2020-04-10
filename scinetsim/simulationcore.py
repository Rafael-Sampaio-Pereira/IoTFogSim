
from collections import defaultdict
from twisted.python import log
import tkinter
from twisted.internet import tksupport
from tkinter import PhotoImage
from config.settings import version
from scinetsim.ScrollableScreen import ScrollableScreen


class SimulationCore(object):
 	
	def __init__(self):
		# self.allWirelessConnections = defaultdict(list)
		self.allConnections = set()
		self.allFogNodes = defaultdict(list)
		self.allCloudNodes = defaultdict(list)
		self.allAccessPointNodes = defaultdict(list)
		self.allIoTNodes = defaultdict(list)
		self.allRouterNodes = defaultdict(list)
		self.allSinkNodes = defaultdict(list)
		self.allSensorNodes = defaultdict(list)
		self.canvas = None
		self.simulation_screen = None
		self.eventsCounter = 0
		self.allProtocols = set()


	def get_any_protocol_by_addr_and_port(self, addr, port):
			try:
				for proto in self.allProtocols:
					if proto.transport.getHost().host == addr and proto.transport.getHost().port == port:
						return proto
			except:
				pass

	def updateEventsCounter(self, event_description):
		self.eventsCounter = self.eventsCounter + 1
		log.msg(event_description+" - Number of events: %i" %(self.eventsCounter))
		# Updates events counter value on screen - Rafael Sampaio
		self.canvas.itemconfig(self.simulation_screen.events_counter_label, text=str(self.eventsCounter))

	def getFogNodeById(self, id):
		try:
			filtered_list = self.allFogNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no fog node whith the id %i"%(id))

	def getCloudNodeById(self, id):
		try:
			filtered_list = self.allCloudNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no cloud node whith the id %i"%(id))

	def getAccessPointNodeById(self, id):
		try:
			filtered_list = self.allAccessPointNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no access point whith the id %i"%(id))

	def getRouterNodeById(self, id):
		try:
			filtered_list = self.allRouterNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no router whith the id %i"%(id))
	
	def getSinkNodeById(self, id):
		try:
			filtered_list = self.allSinkNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no sink whith the id %i"%(id))

	def getSensorNodeById(self, id):
		try:
			filtered_list = self.allSensorNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no sensor whith the id %i"%(id))

	def getIoTNodeById(self, id):
		try:
			filtered_list = self.allIoTNodes[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no IoT node whith the id %i"%(id))

	def getConnectionById(self, id):
		try:
			filtered_list = self.allConnections[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no connection whith the id %i"%(id))

	def getWirelessConnectionById(self, id):
		try:
			filtered_list = self.allWirelessConnections[id]
			return filtered_list[0]
		except Exception as e:
			log.msg("There is no wireless connection whith the id %i"%(id))

	def appendFogNodes(self, fog_node):
		self.allFogNodes[fog_node.id].append(fog_node)

	def appendCloudNodes(self, cloud_node):
		self.allCloudNodes[cloud_node.id].append(cloud_node)

	def appendAccessPointNode(self, ap):
		self.allAccessPointNodes[ap.id].append(ap)

	def appendIoTNodes(self, iot_node):
		self.allIoTNodes[iot_node.id].append(iot_node)

	def appendRouterNodes(self, router_node):
		self.allRouterNodes[router_node.id].append(router_node)

	def appendSinkNodes(self, sink_node):
		self.allSinkNodes[sink_node.id].append(sink_node)

	def appendSensorNodes(self, sensor_node):
		self.allSensorNodes[sensor_node.id].append(sensor_node)

	def appendConnections(self, connection):
		self.allConnections[connection.id].append(connection)

	# def appendWirelessConnections(self, wireless_connection):
	# 	self.allwirelessConnections[wireless_connection.id].append(wireless_connection)

	def getAnyDeviceById(self, id):
		
		if self.getFogNodeById(id):
			if self.getFogNodeById(id).id == id:
				return self.allFogNodes[id][0]

		elif self.getCloudNodeById(id):
			if self.getCloudNodeById(id).id == id:
				return self.allCloudNodes[id][0]

		elif self.getIoTNodeById(id):
			if self.getIoTNodeById(id).id == id:
				return self.allIoTNodes[id][0]

		elif self.getAccessPointNodeById(id):
			if self.getAccessPointById(id).id == id:
				return self.allAccessPointNodes[id][0]

		elif self.getRouterNodeById(id):
			if self.getRouterNodeById(id).id == id:
				return self.allRouterNodes[id][0]
		
		elif self.getSinkNodeById(id):
			if self.getSinkNodeById(id).id == id:
				return self.allSinkNodes[id][0]

		elif self.getSensorNodeById(id):
			if self.getSensorNodeById(id).id == id:
				return self.allSensorNodes[id][0]

		

	def create_simulation_canvas(self):
			
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
		#window.tk.call('wm', 'iconphoto', window._w, PhotoImage(master=window,file='graphics/icons/iotfogsim_icon.png'))
		window.iconphoto(True, PhotoImage(file='graphics/icons/iotfogsim_icon.png'))
		
		# Setting window top text. - Rafael Sampaio
		window.title("IoTFogSim %s - An Distributed Event-Driven Network Simulator"%(version))
		
		# Simulation area on screen. - Rafael Sampaio
		self.simulation_screen = ScrollableScreen(window)
		self.simulation_screen.pack(fill="both", expand=True)
		canvas = self.simulation_screen.getCanvas()

		self.canvas = canvas

		return self.canvas