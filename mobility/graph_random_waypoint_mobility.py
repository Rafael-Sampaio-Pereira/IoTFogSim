import random
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from mobility.mobility_models import MobilityModel
import math
import networkx as nx
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.task import cooperate
import os
import json
from twisted.internet.task import LoopingCall


"""
Model introduction
This extends random waypoint models, but node can only move into a given graph
"""


class GraphRandomWaypointMobility(MobilityModel):
    """Move randomically a visual component icon into graph using the random waypoint mobility model.
                visual_component: A component that contains icon and node info
                min_speed: float - Min value for mobility velocility
                max_speed: float - Max value for mobility velocility
                min_pause: int - Mix pause value for a node stay at a given waypoint
                max_pause: int - Max pause value for a node stay at a given waypoint
            """

    def __init__(self, visual_component,
                 simulation_core,
                 min_speed: float,
                 max_speed: float,
                 min_pause: int,
                 max_pause: int):
        super().__init__(simulation_core)
        self.graph = nx.Graph()
        self.mount_graph()
        self.simulation_core = simulation_core
        self.visual_component = visual_component
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.min_pause = min_pause
        self.max_pause = max_pause
        self.state = 'STOPED'
        self.all_path_trajectory_coordinates = []
        

    @inlineCallbacks
    def start(self):
        # wait few times before node start the mobility, this is to prevent the node.run_mobility be called before put points in list - Rafael Sampaio
        yield sleep(0.5)
        LoopingCall(self.move).start(0.1)
        
    def generate_all_path_coords_points_between_two_points(self):
        
        for source in self.all_mobility_points:
            # Getting source graph node(i.e. vertice) - Rafael Sampaio
            source_point = self.get_graph_node_by_coords(source['x'], source['y'])
            
            for destination in self.all_mobility_points:
                if source != destination:
                    # Getting destiny graph node(i.e. vertice) - Rafael Sampaio
                    destination_point = self.get_graph_node_by_coords(destination['x'], destination['y'])
                    
                    if source_point and destination_point:
                        all_trajectory_coordinates = []
                        # Getting shortest path trajectory between 2 positions and - Rafael Sampaio
                        trajectory_points = nx.shortest_path(self.graph, source_point[0], destination_point[0], weight="weight")
                        
                        # Getting all coords in shortest path trajectory between 2 positions - Rafael Sampaio
                        if destination:
                            first_trajectory_poitnt = None
                            for idx, elem in enumerate(trajectory_points):
                                if not first_trajectory_poitnt:
                                    first_trajectory_poitnt = elem
                                
                                thiselem = elem
                                nextelem = trajectory_points[(idx + 1) % len(trajectory_points)]
                                if first_trajectory_poitnt != nextelem:
                                    all_trajectory_coordinates.extend(
                                        list(
                                            bresenham(
                                                self.graph.nodes[thiselem]['x'],
                                                self.graph.nodes[thiselem]['y'],
                                                self.graph.nodes[nextelem]['x'],
                                                self.graph.nodes[nextelem]['y'],
                                            )
                                        )
                                    )
                                    
                                    # reducing points quantities based on simulation speed
                                    if self.simulation_core.clock.time_speed_multiplier != 1:
                                        final_pos = all_trajectory_coordinates[-1]
                                        n_elements = int(len(all_trajectory_coordinates) * self.simulation_core.clock.time_speed_multiplier/100)
                                        all_trajectory_coordinates = random.sample(
                                            all_trajectory_coordinates,
                                            n_elements
                                        )
                                        all_trajectory_coordinates.append(final_pos)
            
                            coords_data ={
                                'source_point': source_point,
                                'destination_point': destination_point,
                                'trajectory_coordinates': all_trajectory_coordinates
                            }
                            self.all_path_trajectory_coordinates.append(coords_data)
                    
    @inlineCallbacks
    def move(self) -> None:
        all_trajectory_coordinates = None
        # Choosing randomically a waypoint in all_mobility_points list - Rafael Sampaio
        next_random_point = random.choice(self.all_mobility_points)
        
        # Getting destiny graph node(i.e. vertice) - Rafael Sampaio
        destiny_point = self.get_graph_node_by_coords(next_random_point['x'], next_random_point['y'])
        
        # Getting current position - Rafael Sampaio
        current_point = self.get_graph_node_by_coords(self.visual_component.x, self.visual_component.y)
        
        trajectory_data = next(filter(
                                lambda data: data['source_point'] == current_point and data['destination_point'] == destiny_point,
                                self.all_path_trajectory_coordinates), None)
        self.simulation_core.updateEventsCounter(
            f"{self.visual_component.name} moving from x:{self.visual_component.x} y:{self.visual_component.y} coords to x:{next_random_point['x']} y:{next_random_point['y']} coords ")
        
        if trajectory_data:
            all_trajectory_coordinates = trajectory_data['trajectory_coordinates']
            step_speed = random.uniform(self.min_speed, self.max_speed)
            step_speed = self.simulation_core.clock.get_internal_time_unit(step_speed)
            wall_was_found = False
            tolerance = None
            for x, y in all_trajectory_coordinates:
                old_x = self.visual_component.x
                old_y = self.visual_component.y
                # Due it is a loop, verify if last movement has resulted in a wall collision - Rafael Sampaio
                if not wall_was_found:
                    # verify if object just got its destiny - Rafael Sampaio
                    if not(x == next_random_point['x']) and not(y == next_random_point['y']):
                        # preventing icon cross wall - Rafael Sampaio
                        tolerance = 10
                        # Moving icon on screen at - Rafael Sampaio
                        cooperate(self.visual_component.move_on_screen(x, y))
                        if self.simulation_core.scene_adapter:
                            if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                                # if found a collision, then rolling back to old position - Rafael Sampaio
                                reactor.callFromThread(self.visual_component.move_on_screen, old_x, old_y)
                                wall_was_found = True
                                break
                    else:
                        # doing last trajectory movement, so it will pause and after some tim, choose another graph point and play again - Rafael Sampaio
                        self.visual_component.move_on_screen(x, y)
                    yield sleep(step_speed)

            # Stay at point for a random period, so move again to another point - Rafael Sampaio
            pause_time = random.randint(self.min_pause, self.max_pause)
            pause_time = self.simulation_core.clock.get_internal_time_unit(pause_time)
            reactor.callLater(pause_time, self.move)


    @inlineCallbacks 
    def generate_graph_points(self):
        """Distributes the verticies of a desired graph.
            Rafael Sampaio
        """
        log.msg("Info :  - | Generating graph mobility points...")
        # waiting for mobility model object get the simulation core - Rafael Sampaio
        yield sleep(0.5)
        point_size = 20
        first_vertice = None

        file_path = 'projects/'+self.simulation_core.project_name+'/mobility_graph.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as nodes_file:
                data = json.loads(nodes_file.read())
                if data:
                    for vertice in data['vertices']:
                        if not first_vertice:
                            first_vertice = vertice
                        self.add_graph_node(vertice['name'], vertice['x'], vertice['y'])

        # Put icon in the fisrt node of the graph - Rafael Sampaio
        self.visual_component.move_on_screen(first_vertice['x'], first_vertice['y'])
        
        # Drawing points in canvas - Rafael Sampaio
        self.draw_points(point_size)
    
    @inlineCallbacks  
    def generate_graph_edges(self):
        yield sleep(0.5)
        self.add_graph_edge_with_dinamic_weight('IN_1', 'POINT_1')
        self.add_graph_edge_with_dinamic_weight('POINT_1', 'DOOR_1')
        self.add_graph_edge_with_dinamic_weight('DOOR_1', 'POINT_2')
        self.add_graph_edge_with_dinamic_weight('POINT_2', 'DOOR_2')
        self.add_graph_edge_with_dinamic_weight('DOOR_1', 'DOOR_2')
        self.add_graph_edge_with_dinamic_weight('DOOR_2', 'POINT_3')
        self.add_graph_edge_with_dinamic_weight('POINT_3', 'DOOR_3')
        self.add_graph_edge_with_dinamic_weight('DOOR_3', 'DOOR_5')
        self.add_graph_edge_with_dinamic_weight('DOOR_3', 'POINT_4')
        self.add_graph_edge_with_dinamic_weight('POINT_4', 'DOOR_5')
        self.add_graph_edge_with_dinamic_weight('POINT_4', 'DOOR_4')
        self.add_graph_edge_with_dinamic_weight('DOOR_4', 'POINT_5')
        self.add_graph_edge_with_dinamic_weight('DOOR_4', 'DOOR_5')
        self.add_graph_edge_with_dinamic_weight('DOOR_5', 'IN_2')
        self.add_graph_edge_with_dinamic_weight('DOOR_5', 'POINT_6')
        self.add_graph_edge_with_dinamic_weight('DOOR_5', 'DOOR_5A')
        self.add_graph_edge_with_dinamic_weight('IN_2', 'POINT_6')
        self.add_graph_edge_with_dinamic_weight('IN_2', 'DOOR_6')
        self.add_graph_edge_with_dinamic_weight('POINT_6', 'DOOR_5A')
        self.add_graph_edge_with_dinamic_weight('POINT_6', 'DOOR_6')
        self.add_graph_edge_with_dinamic_weight('DOOR_5A', 'POINT_7')
        self.add_graph_edge_with_dinamic_weight('DOOR_5A', 'DOOR_6')
        self.add_graph_edge_with_dinamic_weight('DOOR_6', 'DOOR_7')
        self.add_graph_edge_with_dinamic_weight('DOOR_6', 'DOOR_8')
        self.add_graph_edge_with_dinamic_weight('DOOR_6', 'POINT_8')
        self.add_graph_edge_with_dinamic_weight('POINT_8', 'DOOR_7')
        self.add_graph_edge_with_dinamic_weight('POINT_8', 'DOOR_8')
        self.add_graph_edge_with_dinamic_weight('POINT_9', 'DOOR_7')
        self.add_graph_edge_with_dinamic_weight('POINT_10', 'DOOR_8')

        
    def add_graph_node(self, name, x, y):
        self.graph.add_node(name, x=x, y=y)
        self.all_mobility_points.append({"x": x, "y": y})
    
    @inlineCallbacks
    def mount_graph(self):
        self.generate_graph_points()
        yield sleep(1)
        self.generate_graph_edges()
        yield sleep(1)
        self.generate_all_path_coords_points_between_two_points()
        yield sleep(1)
        cooperate(self.start())
        
    def add_graph_edge_with_dinamic_weight(self, fisrt_node: str, second_node: str):
        # the edge weight will be added calculating the distance between the nodes -Rafael Sampaio
        fisrt_node_name = fisrt_node
        second_node_name = second_node
        fisrt_node = self.graph.nodes[fisrt_node]
        second_node = self.graph.nodes[second_node]
        dist = math.sqrt((second_node['x'] - fisrt_node['x'])**2 + (second_node['y'] - fisrt_node['y'])**2)
        self.graph.add_edge(fisrt_node_name, second_node_name, weight=dist)
        # uncomment the line below to plot edge arrows on the canvas - rafael sampaio
        #self.simulation_core.canvas.create_line(int(fisrt_node['x']), int(fisrt_node['y']), int(second_node['x']), int(second_node['y']), arrow="both", width=3, fill='red')
    
    def get_graph_node_by_coords(self, x, y):
        for node in self.graph.nodes(data=True):
            if node[1]['x'] == x and node[1]['y'] == y:
                return node
