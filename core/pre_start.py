from components.machines import Machine
from components.peripherals import NetworkInterface
import json
import os
from models.human import Human

def load_nodes(project_name, simulation_core):

    with open('projects/'+project_name+'/nodes.json', 'r') as nodes_file:
        data = json.loads(nodes_file.read())

        if data:
            ################## LOADING DEVICES - Rafael Sampaio ##################
            for network in data['networks']:
                for machine in network['machines']:
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
                            machine['coverage_area_radius'],
                            machine['connected_gateway_addrs']
                        )

                    for intf in machine['network_interfaces']:
                        _interface = NetworkInterface(
                            simulation_core,
                            intf['name'],
                            intf['is_wireless'],
                            intf['ip'],
                            _machine
                        )
                        _machine.network_interfaces.append(_interface)
                    simulation_core.all_machines.append(_machine)
                    
                    if machine['type'] == 'router' or machine['type'] == 'switch' or machine['type'] == 'access_point':
                        simulation_core.all_gateways.append(_machine)
                        
                    if machine['type'] == 'server':
                        simulation_core.all_servers.append(_machine)
        
def load_humans(project_name, simulation_core):

    with open('projects/'+project_name+'/humans.json', 'r') as humans_file:
        data = json.loads(humans_file.read())

        if data:
            for human in data:
                _human = Human(
                    name=human['name'],
                    age=human['age'],
                    icon=human['icon'],
                    x=human['x'],
                    y=human['y'],
                    weight=human['weight'],
                    height=human['height'],
                    simulation_core=simulation_core,
                )
                simulation_core.all_humans.append(_human)