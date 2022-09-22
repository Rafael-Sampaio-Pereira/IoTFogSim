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
        self.start()

    @inlineCallbacks
    def start(self):
        # wait few times before node start the mobility, this is to prevent the node.run_mobility be called before put points in list - Rafael Sampaio
        yield sleep(0.5)
        self.move()

    @inlineCallbacks
    def move(self) -> None:

        all_coordinates_between_two_points = []
        # Choosing randomically a waypoint in all_mobility_points list - Rafael Sampaio
        next_random_point = random.choice(self.all_mobility_points)
        # Getting all coords between current node(visual_component) position and the selected next point - Rafael Sampaio
        if next_random_point:
            all_coordinates_between_two_points = list(
                bresenham(self.visual_component.x, self.visual_component.y, next_random_point['x'], next_random_point['y']))

            self.simulation_core.updateEventsCounter(
                f"Mobile Node {self.visual_component.deviceName} Moving to x:{next_random_point['x']} y:{next_random_point['y']} coords ")

            step_speed = random.uniform(self.min_speed, self.max_speed)
            wall_was_found = False
            tolerance = None
            for x, y in all_coordinates_between_two_points:
                old_x = self.visual_component.x
                old_y = self.visual_component.y
                # Due it is a loop, verify if last movement has resulted in a wall collision - Rafael Sampaio
                if not wall_was_found:
                    # verify if object just got its destiny - Rafael Sampaio
                    if not(x == next_random_point['x']) and not(y == next_random_point['y']):
                        # preventing icon cross wall - Rafael Sampaio
                        tolerance = 10
                        # Moving icon on screen at - Rafael Sampaio
                        self.visual_component.move_on_screen(x, y)
                        if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                            # if found a collision, then rolling back to old position - Rafael Sampaio
                            self.visual_component.move_on_screen(
                                old_x, old_y)
                            wall_was_found = True
                            break
                    yield sleep(step_speed)

            # Stay at point for a random period, so move again to another point - Rafael Sampaio
            self.simulation_core.canvas.after(random.randint(
                self.min_pause, self.max_pause), self.move)
            
    @inlineCallbacks 
    def generate_graph_points(self):
        """Distributes of a desired graph.
            Rafael Sampaio
        """
        log.msg("Info : - | Generating graph mobility points...")
        # waiting for mobility model object get the simulation core - Rafael Sampaio
        yield sleep(0.5)
        point_size = 40
        self.add_graph_node("A", x=200, y=100)
        self.add_graph_node("B", x=300, y=555)
        self.add_graph_node("C", x=240, y=98)
        self.add_graph_node("D", x=59, y=600)
        # Drawing points in canvas - Rafael Sampaio
        self.draw_points(point_size)
    
    @inlineCallbacks  
    def generate_graph_edges(self):
        yield sleep(0.5)
        self.add_graph_edge_with_dinamic_weight('A', 'B')
        self.add_graph_edge_with_dinamic_weight('B', 'D')
        self.add_graph_edge_with_dinamic_weight('A', 'C')
        self.add_graph_edge_with_dinamic_weight('C', 'D')
        
    def add_graph_node(self, name, x, y):
        self.graph.add_node(name, x=x, y=y)
        self.all_mobility_points.append({"x": x, "y": y})
    
    @inlineCallbacks
    def mount_graph(self):
        self.generate_graph_points()
        yield sleep(1)
        self.generate_graph_edges()
        
        
        
        
    def add_graph_edge_with_dinamic_weight(self, fisrt_node: str, second_node: str):
        # the edge weight will be added calculating the distance between the nodes -Rafael Sampaio
        fisrt_node_name = fisrt_node
        second_node_name = second_node
        fisrt_node = self.graph.nodes[fisrt_node]
        second_node = self.graph.nodes[second_node]
        dist = math.sqrt((second_node['x'] - fisrt_node['x'])**2 + (second_node['y'] - fisrt_node['y'])**2)
        self.graph.add_edge(fisrt_node_name, second_node_name, weight=dist)
        self.simulation_core.canvas.create_line(int(fisrt_node['x']), int(fisrt_node['y']), int(second_node['x']), int(second_node['y']), arrow="both", width=3, fill='red')
    
    def get_graph_node_by_coords(self, x, y):
        for node in self.graph.nodes(data=True):
            if node[1]['x'] == x and node[1]['y'] == y:
                return node

    



    # result = nx.shortest_path(G, "A", "D", weight="weight")
    # print(result)
    # # print(G.nodes['B']['x'])

    # _node = get_graph_node_by_coords(G, 1,5)
