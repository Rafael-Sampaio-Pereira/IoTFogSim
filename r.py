import json


with open('nodes.js') as nodes:
    nodes = json.load(nodes)
    for fog_node in nodes['fog_nodes']:

        print('Fog node addr: ' + fog_node['website'])