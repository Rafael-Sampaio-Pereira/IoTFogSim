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
import time
import numpy as np


class TaskBasedGraphRandomWaypointMobility(MobilityModel):
    """Move a visual component icon into graph based on task point.
                visual_component: A component that contains icon and node info
                min_speed: float - Min value for mobility velocility
                max_speed: float - Max value for mobility velocility
            """

    def __init__(self, visual_component,
                simulation_core,
                min_speed: float,
                max_speed: float,
                actor):
        super().__init__(simulation_core)
        self.all_mobility_points = []
        self.actor = actor
        
        self.graph = nx.Graph()
        self.mount_graph()
        self.simulation_core = simulation_core
        self.visual_component = visual_component
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.all_path_trajectory_coordinates = []
        self.next_mobility_point = None

    def start(self):
        pass
        
    def generate_all_path_coords_points_between_two_points(self):
        
        for source in self.all_mobility_points:
            # Getting source graph node(i.e. vertice)
            source_point = self.get_graph_node_by_coords(source['x'], source['y'])
            
            for destination in self.all_mobility_points:
                if source != destination:
                    # Getting destiny graph node(i.e. vertice)
                    destination_point = self.get_graph_node_by_coords(destination['x'], destination['y'])
                    
                    if source_point and destination_point:
                        all_trajectory_coordinates = []
                        # Getting shortest path trajectory between 2 positions and
                        trajectory_points = nx.shortest_path(self.graph, source_point[0], destination_point[0], weight="weight")
                        
                        # Getting all coords in shortest path trajectory between 2 positions
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
                                        if self.simulation_core.global_seed:
                                            random.seed(self.simulation_core.global_seed)
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
                        
    def set_next_mobility_point(self, point_name):
        self.next_mobility_point = next(filter(
                lambda point: point["name"] == point_name,
                self.all_mobility_points), None)
                    
    @inlineCallbacks
    def move(self) -> None:
        
        if self.simulation_core.is_running:
            # Getting current position
            current_point = self.get_graph_node_by_coords(self.visual_component.x, self.visual_component.y)
                        
            all_trajectory_coordinates = None
            next_point = None
            if self.next_mobility_point:
                next_point = self.next_mobility_point 
                self.next_mobility_point = None

                # Shuffling points list to avoid duplicates choices
                random.shuffle(self.all_mobility_points)
                    
                # Getting destiny graph node(i.e. vertice)
                destiny_point = self.get_graph_node_by_coords(next_point['x'], next_point['y'])
                
                trajectory_data = next(filter(
                                        lambda data: data['source_point'] == current_point and data['destination_point'] == destiny_point,
                                        self.all_path_trajectory_coordinates), None)
                self.simulation_core.updateEventsCounter(
                    f"{self.visual_component.name} moving from x:{self.visual_component.x} y:{self.visual_component.y} coords to x:{next_point['x']} y:{next_point['y']} coords ")
                
                if trajectory_data:
                    print("TEM DADOS DE TRAJETORIA")
                    all_trajectory_coordinates = trajectory_data['trajectory_coordinates']
                    if self.simulation_core.global_seed:
                        random.seed(self.simulation_core.global_seed)
                    step_speed = random.uniform(self.min_speed, self.max_speed)
                    step_speed = self.simulation_core.clock.get_internal_time_unit(step_speed)
                    wall_was_found = False

                    for x, y in all_trajectory_coordinates:
                        # Due it is a loop, verify if last movement has resulted in a wall collision
                        if not wall_was_found:
                            # verify if object just got its destiny
                            if not(x == next_point['x']) and not(y == next_point['y']):
                                # Moving icon on screen at
                                self.visual_component.move_on_screen(x, y)
                                
                            else:
                                # doing last trajectory movement
                                self.visual_component.move_on_screen(x, y)
                            yield sleep(step_speed)
                            
                    del all_trajectory_coordinates
                    del trajectory_data


    @inlineCallbacks 
    def generate_graph_points(self):
        """Distributes the verticies of a desired graph."""
        log.msg("Info :  - | Generating graph mobility points...")
        # waiting for mobility model object get the simulation core
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

        # Put icon in the fisrt node of the graph
        self.visual_component.move_on_screen(first_vertice['x'], first_vertice['y'])
        
        # Drawing points in canvas
        self.draw_points(point_size)
    
    @inlineCallbacks  
    def generate_graph_edges(self):
        yield sleep(0.5)
        file_path = 'projects/'+self.simulation_core.project_name+'/mobility_graph.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as nodes_file:
                data = json.loads(nodes_file.read())
                if data:
                    for edge in data['edges']:
                        self.add_graph_edge_with_dinamic_weight(edge['vertice_1'], edge['vertice_2'])


        
    def add_graph_node(self, name, x, y):
        self.graph.add_node(name, x=x, y=y)
        self.all_mobility_points.append({"name": name, "x": x, "y": y})
    
    @inlineCallbacks
    def mount_graph(self):
        self.generate_graph_points()
        yield sleep(1)
        self.generate_graph_edges()
        yield sleep(1)
        self.generate_all_path_coords_points_between_two_points()
        yield sleep(1)
        # cooperate(self.start())
        self.start()
        
    def add_graph_edge_with_dinamic_weight(self, fisrt_node: str, second_node: str):
        # the edge weight will be added calculating the distance between the nodes
        fisrt_node_name = fisrt_node
        second_node_name = second_node
        fisrt_node = self.graph.nodes[fisrt_node]
        second_node = self.graph.nodes[second_node]
        dist = math.sqrt((second_node['x'] - fisrt_node['x'])**2 + (second_node['y'] - fisrt_node['y'])**2)
        self.graph.add_edge(fisrt_node_name, second_node_name, weight=dist)
        # uncomment the line below to plot edge arrows on the canvas
        self.simulation_core.canvas.create_line(
            int(fisrt_node['x']),
            int(fisrt_node['y']),
            int(second_node['x']),
            int(second_node['y']),
            arrow="both",
            dash=(4,2),
            width=1,
            fill='#F0F4D3'
        )
    
    def get_graph_node_by_coords(self, x, y):
        for node in self.graph.nodes(data=True):
            if node[1]['x'] == x and node[1]['y'] == y:
                return node
