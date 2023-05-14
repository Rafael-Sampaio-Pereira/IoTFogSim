import random
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from mobility.mobility_models import MobilityModel
from twisted.internet import reactor


"""
Model introduction
In mobility management, the random waypoint model is a random model that simulates the movement 
of mobile users and how their position, speed, and acceleration change over time. When evaluating 
new network protocols, mobility models are used for simulation purposes. Random Waypoint Model(RWP) 
was originally proposed by Johnson and Maltz. Due to its simplicity and wide availability, it is 
one of the most popular mobile models for evaluating mobile ad hoc network (MANET) routing 
protocols. In the random-based mobility simulation model, mobile nodes move randomly and freely 
without restriction. More specifically, the destination, speed, and direction are randomly selected 
and independent of other nodes. This model has been used in many simulation studies. There are two 
variants of RWP: random walk model (RW) and random direction model (RD). The following describes 
RWP and its two variants.

1.1 Random Waypoint Model
In RWP, in the initial state, the nodes are uniformly distributed throughout the simulation area. 
The nodes first randomly select a node from the two-dimensional simulation area as the destination,
and then select [Vmin, Vmax] Randomly select a speed (subject to uniform distribution), and the 
node will move to the destination at this speed. After reaching the destination, the node is at 
[0, Pmax] Randomly select a period of stay time T, and then select the next destination.  

found at: https://www.big-meter.com/opensource/en/5ff4abd139fb6523f2624e91.html
"""


class RandomWaypointMobility(MobilityModel):
    """Move randomically a visual component icon on canvas using the random waypoint mobility model.
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
        self.generate_distributed_random_points()
        self.simulation_core = simulation_core
        self.visual_component = visual_component
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.min_pause = min_pause
        self.max_pause = max_pause
        self.start()

    @inlineCallbacks
    def start(self):
        # wait few times before node start the mobility, this is to prevent the node.run_mobility be called before put points in list
        yield sleep(0.5)
        self.move()

    @inlineCallbacks
    def move(self) -> None:

        all_coordinates_between_two_points = []
        # Choosing randomically a waypoint in all_mobility_points list
        next_random_point = random.choice(self.all_mobility_points)
        # Getting all coords between current node(visual_component) position and the selected next point
        if next_random_point:
            all_coordinates_between_two_points = list(
                bresenham(self.visual_component.x, self.visual_component.y, next_random_point['x'], next_random_point['y']))

            # reducing points quantities based on simulation speed
            if self.simulation_core.clock.time_speed_multiplier != 1:
                final_pos = all_coordinates_between_two_points[-1]
                n_elements = int(len(all_coordinates_between_two_points) * self.simulation_core.clock.time_speed_multiplier/100)
                all_coordinates_between_two_points = random.sample(
                    all_coordinates_between_two_points,
                    n_elements
                )
                all_coordinates_between_two_points.append(final_pos)


            self.simulation_core.updateEventsCounter(
                f"Mobile Node {self.visual_component.name} Moving to x:{next_random_point['x']} y:{next_random_point['y']} coords ")

            step_speed = random.uniform(self.min_speed, self.max_speed)
            step_speed = self.simulation_core.clock.get_internal_time_unit(step_speed)
            wall_was_found = False
            tolerance = None
            for x, y in all_coordinates_between_two_points:
                old_x = self.visual_component.x
                old_y = self.visual_component.y
                # Due it is a loop, verify if last movement has resulted in a wall collision
                if not wall_was_found:
                    # verify if object just got its destiny
                    if not(x == next_random_point['x']) and not(y == next_random_point['y']):
                        # preventing icon cross wall
                        tolerance = 5
                        # Moving icon on screen at
                        self.visual_component.move_on_screen(x, y)
                        if self.simulation_core.scene_adapter and self.simulation_core.scene_adapter.ground_plan:
                            if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                                # if found a collision, then rolling back to old position
                                self.visual_component.move_on_screen(
                                    old_x, old_y)
                                wall_was_found = True
                                break
                    yield sleep(step_speed)

            # Stay at point for a random period, so move again to another point
            pause_time = random.randint(self.min_pause, self.max_pause)
            pause_time = self.simulation_core.clock.get_internal_time_unit(pause_time)
            reactor.callLater(pause_time, self.move)
