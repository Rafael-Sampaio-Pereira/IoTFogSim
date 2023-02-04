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
        

    @inlineCallbacks
    def start(self):
        # wait few times before node start the mobility, this is to prevent the node.run_mobility be called before put points in list - Rafael Sampaio
        yield sleep(0.5)
        LoopingCall(self.move).start(0.1)

    @inlineCallbacks
    def move(self) -> None:
        all_trajectory_coordinates = []
        # Choosing randomically a waypoint in all_mobility_points list - Rafael Sampaio
        next_random_point = random.choice(self.all_mobility_points)
        
        # Getting destiny graph node(i.e. vertice) - Rafael Sampaio
        destiny_point = self.get_graph_node_by_coords(next_random_point['x'], next_random_point['y'])
        
        # Getting current position - Rafael Sampaio
        current_point = self.get_graph_node_by_coords(self.visual_component.x, self.visual_component.y)
        
        # Getting shortest path trajectory between current node(visual_component) position and the selected next point - Rafael Sampaio
        trajectory_points = nx.shortest_path(self.graph, current_point[0], destiny_point[0], weight="weight")
        
        # Getting all coords in shortest path trajectory between current node(visual_component) position and the selected next point - Rafael Sampaio
        if next_random_point:
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
            self.simulation_core.updateEventsCounter(
                f"{self.visual_component.name} moving from x:{self.visual_component.x} y:{self.visual_component.y} coords to x:{next_random_point['x']} y:{next_random_point['y']} coords ")

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
            
        # if not self.state == 'MOVING' or not self.state == 'PAUSED':
        #     self.state = 'MOVING'
        #     all_trajectory_coordinates = []
        #     # Choosing randomically a waypoint in all_mobility_points list - Rafael Sampaio
        #     next_random_point = random.choice(self.all_mobility_points)
            
        #     # Getting destiny graph node(i.e. vertice) - Rafael Sampaio
        #     destiny_point = self.get_graph_node_by_coords(next_random_point['x'], next_random_point['y'])
            
        #     # Getting current position - Rafael Sampaio
        #     current_point = self.get_graph_node_by_coords(self.visual_component.x, self.visual_component.y)
            
        #     # Getting shortest path trajectory between current node(visual_component) position and the selected next point - Rafael Sampaio
        #     trajectory_points = nx.dijkstra_path(self.graph, current_point[0], destiny_point[0], weight="weight")
            
        #     # Getting all coords in shortest path trajectory between current node(visual_component) position and the selected next point - Rafael Sampaio
        #     if next_random_point:
        #         first_trajectory_poitnt = None
        #         for idx, elem in enumerate(trajectory_points):
        #             if not first_trajectory_poitnt:
        #                 first_trajectory_poitnt = elem
                    
        #             thiselem = elem
        #             nextelem = trajectory_points[(idx + 1) % len(trajectory_points)]
        #             if first_trajectory_poitnt != nextelem:
        #                 all_trajectory_coordinates.extend(
        #                     list(
        #                         bresenham(
        #                             self.graph.nodes[thiselem]['x'],
        #                             self.graph.nodes[thiselem]['y'],
        #                             self.graph.nodes[nextelem]['x'],
        #                             self.graph.nodes[nextelem]['y'],
        #                         )
        #                     )
        #                 )

        #         self.simulation_core.updateEventsCounter(
        #             f"{self.visual_component.name} moving from x:{self.visual_component.x} y:{self.visual_component.y} coords to x:{next_random_point['x']} y:{next_random_point['y']} coords ")

        #         step_speed = random.uniform(self.min_speed, self.max_speed)
        #         step_speed = self.simulation_core.clock.get_internal_time_unit(step_speed)
        #         wall_was_found = False
        #         tolerance = None
        #         for x, y in all_trajectory_coordinates:
        #             old_x = self.visual_component.x
        #             old_y = self.visual_component.y
        #             # Due it is a loop, verify if last movement has resulted in a wall collision - Rafael Sampaio
        #             if not wall_was_found:
        #                 # verify if object just got its destiny - Rafael Sampaio
        #                 if not(x == next_random_point['x']) and not(y == next_random_point['y']):
        #                     # preventing icon cross wall - Rafael Sampaio
        #                     tolerance = 10
        #                     # Moving icon on screen at - Rafael Sampaio
        #                     cooperate(self.visual_component.move_on_screen(x, y))
        #                     if self.simulation_core.scene_adapter:
        #                         if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
        #                             # if found a collision, then rolling back to old position - Rafael Sampaio
        #                             reactor.callFromThread(self.visual_component.move_on_screen, old_x, old_y)
        #                             wall_was_found = True
        #                             break
        #                 else:
        #                     # doing last trajectory movement, so it will pause and after some tim, choose another graph point and play again - Rafael Sampaio
        #                     self.visual_component.move_on_screen(x, y)
        #                     # Stay at point for a random period, so move again to another point - Rafael Sampaio
        #                     pause_time = random.randint(self.min_pause, self.max_pause)
        #                     pause_time = self.simulation_core.clock.get_internal_time_unit(pause_time)
        #                     self.state = 'PAUSED'
        #                     yield sleep(pause_time)
        #                     self.state = 'IDLE'
        #                 yield sleep(step_speed)
        #     del trajectory_points
        #     del all_trajectory_coordinates


    @inlineCallbacks 
    def generate_graph_points(self):
        """Distributes the verticies of a desired graph.
            Rafael Sampaio
        """
        log.msg("Info :  - | Generating graph mobility points...")
        # waiting for mobility model object get the simulation core - Rafael Sampaio
        yield sleep(0.5)
        point_size = 0
        self.add_graph_node("IN_1", x=124, y=180)
        self.add_graph_node("IN_2", x=765, y=824)
        
        self.add_graph_node("DOOR_1", x=377, y=180)
        self.add_graph_node("DOOR_2", x=507, y=311)
        self.add_graph_node("DOOR_3", x=507, y=565)
        self.add_graph_node("DOOR_4", x=255, y=565)
        self.add_graph_node("DOOR_5", x=638, y=696)
        self.add_graph_node("DOOR_5A", x=770, y=311)
        self.add_graph_node("DOOR_6", x=892, y=434)
        self.add_graph_node("DOOR_7", x=1024, y=311)
        self.add_graph_node("DOOR_8", x=1024, y=565)
        
        self.add_graph_node("POINT_1", x=243, y=180)
        self.add_graph_node("POINT_2", x=508, y=180)
        self.add_graph_node("POINT_3", x=508, y=434)
        self.add_graph_node("POINT_4", x=377, y=696)
        self.add_graph_node("POINT_5", x=243, y=434)
        self.add_graph_node("POINT_6", x=761, y=565)
        self.add_graph_node("POINT_7", x=761, y=180)
        self.add_graph_node("POINT_8", x=1024, y=434)
        self.add_graph_node("POINT_9", x=1024, y=180)
        self.add_graph_node("POINT_10", x=1024, y=696)
        
        # Put icon in the fisrt node of the graph - Rafael Sampaio
        self.visual_component.move_on_screen(124, 180)
        
        # Drawing points in canvas - Rafael Sampaio
        # self.draw_points(point_size)
    
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
