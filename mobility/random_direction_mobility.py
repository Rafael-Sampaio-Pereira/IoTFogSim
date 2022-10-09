import random
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from mobility.mobility_models import MobilityModel
from twisted.internet import reactor


"""
Random Direction Model
In RD, the node randomly selects a direction from [0, 2π], and then moves in this direction until 
it reaches the boundary of the simulation area, at [0, Pmax] Randomly select a period of stay 
time T, then select an angle from [0, π], and continue to move. RD can overcome the density wave 
phenomenon caused by RWP.

found at: https://www.big-meter.com/opensource/en/5ff4abd139fb6523f2624e91.html
"""


class RandomDirectionMobility(MobilityModel):
    """Move randomically a visual component icon on canvas using the random direction mobility model.
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
        self.generate_area_border_points()
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
        # Choosing randomically a border point in all_mobility_points list - Rafael Sampaio
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
            reactor.callLater(random.randint(
                self.min_pause, self.max_pause), self.move)
