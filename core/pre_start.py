from core.components import Machine
import json
import os

def load_nodes(project_name, simulation_core):

    with open('projects/'+project_name+'/nodes.json', 'r') as nodes_file:
        data = json.loads(nodes_file.read())

        if data:
            ################## LOADING DEVICES - Rafael Sampaio ##################
            for machine in data['machines']:
                _machine = Machine(
                        simulation_core,
                        machine['name'],
                        machine['MIPS'],
                        machine['icon'],
                        machine['is_wireless'],
                        machine['x'],
                        machine['y'],
                        machine['application'],
                        machine['type'],
                        machine['coverage_area_radius']
                    )
                simulation_core.all_machines.add(_machine)
                


# links_file = "./projects/"+simulation_core.project_name+"/links.json"
# # verify if user has configured an link for current server - Rafael Sampaio
# if 'link' in server.keys():
#     # verify if the links.json file exists - Rafael Sampaio
#     if os.path.isfile(links_file):
#         with open(links_file, 'r') as file:
#             links = json.loads(file.read())
#             for link in links:
#                 if server['link'] == link['name']:
#                     # configure network settings in localhost(loopback) - Rafael Sampaio
#                     sr.confirure_network_link(link['name'],
#                                                 link['transmission_rate'],
#                                                 link['latency'],
#                                                 link['packet_loss'],
#                                                 "lo")

#                     # getting default network interface(e.g. eth0, wlp0) - Rafael Sampaio
#                     default_interface = get_default_interface()

#                     # configure network settings in default network interface - Rafael Sampaio
#                     sr.confirure_network_link(link['name'],
#                                                 link['transmission_rate'],
#                                                 link['latency'],
#                                                 link['packet_loss'],
#                                                 default_interface)

#     else:
#         log.msg("There is no links.json file in this project.")
# else:
#     log.msg(
#         f"Info : - | The network link was not configured for the server on port {server['port']}")