from datetime import datetime
import time
import random
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.task import deferLater
from core.functions import sleep
from twisted.python import log


class MobilityModel(object):

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.n_points = 33
        self.area_max_width = 1000
        self.area_max_height = 1000
        self.all_mobility_points = []

    def draw_points(self, point_size):
        """Draw all mobility points on canvas."""
        for point in self.all_mobility_points:
            # Drawing circles on canvas to represents every point coords - Rafael Sampaio
            self.simulation_core.canvas.create_oval(
                point['x'], point['y'], point['x']+point_size, point['y']+point_size, outline="red", dash=(4, 3))

    @inlineCallbacks
    def generate_distributed_random_points(self):
        """Distributes points using uniform distribution.
            n_points: num of points to be distributed into a given area
            area_max_width: max width of desired area
            area_max_height: max height of desired area
            Rafael Sampaio
        """
        log.msg("Info : - | Generating mobility points...")
        # waiting for mobility model object get the simulation core - Rafael Sampaio
        yield sleep(0.5)
        point_size = 20
        for point in range(1, self.n_points+1):
            # Casting to int due uniform distribution returns float - Rafael Sampaio
            x = int(random.uniform(50, self.area_max_width))
            y = int(random.uniform(50, self.area_max_height))

            # Avoiding to place points into walls - Rafael Sampaio
            if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance=point_size):
                x += point_size+self.simulation_core.scene_adapter.ground_plan.wall_tickness
                y += point_size+self.simulation_core.scene_adapter.ground_plan.wall_tickness

            self.all_mobility_points.append({"x": x, "y": y})
        # Drawing points in canvas - Rafael Sampaio
        self.draw_points(point_size)

    def find_directions_based_on_coords(self, visual_component, x, y):
        """Return two direc tions based on coords."""
        x_direction = None
        y_direction = None
        if x > visual_component.x:
            x_direction = 'RIGHT'
        else:
            x_direction = 'LEFT'

        if y > visual_component.y:
            y_direction = 'DOWN'
        else:
            y_direction = 'UP'

        return x_direction, y_direction


class RandomMobility(MobilityModel):
    """Move randomically a visual component icon on canvas.
        visual_component: A component that contains icon and node info
    """

    def __init__(self, visual_component, simulation_core):
        super().__init__(simulation_core)
        self.simulation_core = simulation_core
        self.visual_component = visual_component
        self.start()

    @inlineCallbacks
    def start(self):
        # wait few times before node start the mobility, this is to prevent the node.run_mobility be called before scene be mounted - Rafael Sampaio
        yield sleep(0.5)
        LoopingCall(self.move).start(0.2)

    def move(self):
        # moving the device icon in canvas in random way - Rafael Sampaio
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
        directions = [UP, DOWN, LEFT, RIGHT]
        direction = random.choice(directions)
        reference = random.randint(50, 100)

        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = None
        y2 = None
        tolerance = 0

        if direction == UP:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.y - reference) < 1:
                y2 = y1 - reference
                x2 = x1

        elif direction == DOWN:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.y + reference) > self.simulation_core.canvas.winfo_height():
                y2 = y1 + reference
                x2 = x1
                # preventin icon cross down wall, adds icon height to prevet wall cross error - Rafael Sampaio
                tolerance = self.visual_component.height

        elif direction == LEFT:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.x - reference) < 1:
                x2 = x1 - reference
                y2 = y1

        elif direction == RIGHT:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.x + reference) > self.simulation_core.canvas.winfo_width():
                x2 = x1 + reference
                y2 = y1
                # preventin icon cross right wall - Rafael Sampaio
                tolerance = self.visual_component.width

        if x2 and y2:
            all_coordinates_between_two_points = list(
                bresenham(x1, y1, x2, y2))
            wall_was_found = False
            for x, y in all_coordinates_between_two_points:
                old_x = self.visual_component.x
                old_y = self.visual_component.y
                if not wall_was_found:
                    # verify if object just got its destiny - Rafael Sampaio
                    if not(x == x2 and y == y2):
                        self.visual_component.move_on_screen(x, y)
                        if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                            # if found a collision, then rolling back to old position - Rafael Sampaio
                            self.visual_component.move_on_screen(
                                old_x, old_y)
                            wall_was_found = True


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
