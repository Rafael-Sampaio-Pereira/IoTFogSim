
from collections import defaultdict


class SimulationCore(object):
 	
	def __init__(self):
		self.allWirelessConnections = defaultdict(list)
		self.allConnections = defaultdict(list)
		self.allFogNodes = defaultdict(list)
		self.allCloudNodes = defaultdict(list)
		self.allAccessPointsNode = defaultdict(list)
		#allRoutersNodes = defaultdict(list)
		self.allIoTNodes = defaultdict(list)
		self.allRoutersNodes = defaultdict(list)

	def getFogNodeById(self, id):
		filtered_list = self.allFogNodes[id]
		print(self.allFogNodes[id][0].id)
		return filtered_list[0]

	def getCloudNodeById(self, id):
		filtered_list = self.allCloudNodes[id]
		return filtered_list[0]

	def getAccessPointById(self, id):
		filtered_list = self.allAccessPointNodes[id]
		return filtered_list[0]

	def getRouterNodeById(self, id):
		filtered_list = self.allRouterNodes[id]
		return filtered_list[0]

	def getIoTNodeById(self, id):
		filtered_list = self.allIoTNodes[id]
		return filtered_list[0]

	def getConnectionById(self, id):
		filtered_list = self.allConnections[id]
		return filtered_list[0]

	def getWirelessConnectionById(self, id):
		filtered_list = self.allWirelessConnections[id]
		return filtered_list[0]

	def appendFogNode(self, fog_node):
		self.allFogNodes[fog_node.id].append(fog_node)

	def appendCloudNode(self, cloud_node):
		self.allCloudNodes[cloud_node.id].append(cloud_node)

	def appendAccessPointNodes(self, ap):
		self.allAccessPointNodes[ap.id].append(ap)

	def appendIoTNodes(self, iot_node):
		self.allIoTNodes[iot_node.id].append(iot_node)

	def appendRouterNodes(self, router_node):
		self.allRouterNodes[router_node.id].append(router_node)



# classe para fins de estudos
class Node(object):
	def __init__(self, name, id):
		self.name = name
		self.id = id

# Demostração de uso
n1 = Node('computer',1)
sc = SimulationCore()
sc.appendFogNode(n1)
nd = sc.getFogNodeById(n1.id)
print(nd.name)