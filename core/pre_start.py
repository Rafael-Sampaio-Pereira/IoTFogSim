from components.machines import Machine
from components.peripherals import NetworkInterface
from components.links import Link
import json
import os
from models.human import Human

def load_nodes(project_name, simulation_core):

    with open('projects/'+project_name+'/nodes.json', 'r') as nodes_file:
        data = json.loads(nodes_file.read())

        if data:
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
                            machine['power_watts']
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
                        simulation_core.all_network_interfaces.append(_interface)
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
                

def load_links(project_name, simulation_core):

    with open('projects/'+project_name+'/links.json', 'r') as links_file:
        data = json.loads(links_file.read())

        if data:
            for link in data:
                itf1 = simulation_core.get_network_interface_by_ip(link["network_interface_1"])
                itf2 = simulation_core.get_network_interface_by_ip(link["network_interface_2"])
                if itf1 and itf2:
                    if not itf1.machine.verify_if_connection_link_already_exists(itf2.machine):
                        _link = Link(simulation_core=simulation_core)
                        _link.name = link['name']
                        _link.bandwidth = link['bandwidth']
                        _link.packet_loss_rate = link['packet_loss_rate']
                        _link.network_interface_1 = itf1
                        _link.network_interface_2 = itf2
                        _link.delay_upper_bound = link['delay_upper_bound']
                        _link.delay_lower_bound = link['delay_lower_bound']
                        _link.delay_mean = link['delay_mean']
                        _link.delay_standard_deviation = link['delay_standard_deviation']
                        simulation_core.all_links.append(_link)
                        itf1.machine.peers.append(itf2.machine)
                        itf2.machine.peers.append(itf1.machine)
                        itf1.machine.links.append(_link)
                        itf2.machine.links.append(_link)
                        _link.draw_connection_arrow()
                        
                        if (itf1.machine.type == 'router' or itf1.machine.type == 'switch' or itf1.machine.type == 'access_point') and (itf2.machine.type == 'router' or itf2.machine.type == 'switch' or itf2.machine.type == 'access_point'):
                            itf1.machine.app.neighbor_gateways.append(itf2.machine)
                            itf2.machine.app.neighbor_gateways.append(itf1.machine)
                            
                            
                            
def load_appliances(project_name, simulation_core):

    with open('projects/'+project_name+'/appliances.json', 'r') as appliances_file:
        data = json.loads(appliances_file.read())

        if data:
            for machine in data:
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
                        machine['power_watts']
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
                    simulation_core.all_network_interfaces.append(_interface)
                simulation_core.all_machines.append(_machine)
