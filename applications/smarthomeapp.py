from datetime import datetime
import time
from tkinter import RIGHT
from turtle import right
from applications.mobilityapp import MobileProducerApp
import random
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.task import deferLater


def sleep(secs):
    """Provide a non-blocking sleep function.
        any method that will use that function inside needs to use the @inlineCallbacks decorator.
        Example: it can be use to control a for iteration time.
        secs: float - Number of seconds to be waiting.
    """
    return deferLater(reactor, secs, lambda: None)


class SmartHomeAdapter(object):
    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.ground_plan = SimpleGroundPlan(simulation_core)
        self.mobility_model = MobilityModel(simulation_core)


class SimpleGroundPlan(object):
    """Ground Plan for simulate house envirioment in smart home context."""

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.wall_tickness = 20
        self.wall_color = "black"

        self.draw_wall(50, 100, 1020, "v")
        self.draw_wall(600, 100, 350, "v")
        self.draw_wall(1000, 100, 1020, "v")

        self.draw_wall(50, 100, 800, "h")
        self.draw_wall(50, 500, 600, "h")
        self.draw_wall(50, 700, 600, "h")
        self.draw_wall(50, 1000, 1020, "h")

    def draw_wall(self, start_x: int, start_y: int, wall_width: int, orientation: str):
        if orientation not in ["v", "h"]:
            raise Exception(
                "Orientation field must be vertical or horizontal.")

        if orientation == "v":
            self.simulation_core.canvas.create_rectangle(start_x, start_y, start_x+self.wall_tickness, wall_width,
                                                         fill=self.wall_color, width=1, tags=("wall",))
        else:
            self.simulation_core.canvas.create_rectangle(start_x, start_y, wall_width, start_y+self.wall_tickness,
                                                         fill=self.wall_color, width=1, tags=("wall",))

    def blink_wall(self, wall):
        original_color = self.simulation_core.scene_adapter.ground_plan.wall_color
        self.simulation_core.canvas.itemconfig(wall, fill="red")
        reactor.callLater(
            0.7, self.simulation_core.canvas.itemconfig, wall, fill=original_color)

    def verify_wall_collision(self, x, y, tolerance):
        if not tolerance:
            tolerance = 0

        # finding all the wifi devices on the canvas screen. - Rafael Sampaio
        all_wall = self.simulation_core.canvas.find_withtag("wall")
        collision_items = self.simulation_core.canvas.find_overlapping(
            x + tolerance,
            y + tolerance,
            x + tolerance,
            y + tolerance
        )

        for wall in all_wall:
            if wall in collision_items:
                self.blink_wall(wall)
                return True
        return False


class PersonDataProducerApp(MobileProducerApp):
    """
#     This is based on in the MQTT MobileProducerApp.
#     This Acts as a Publisher component send tasks to the 'task' mqtt topic.
#     This generates MIPS task and send to OchesrtrationBrokerApp, so broker can
#     send tasks to computeApps(Subscribers)
#     """

    # @override
    def generate_data(self):
        data = '{"coords": {"lat": 56.0000, "lng": 44.0000}}'
        return data

    # @override
    def run_mobility(self):
        # self.simulation_core.scene_adapter.mobility_model.random_mobility(
        #     self.visual_component)
        self.simulation_core.scene_adapter.mobility_model.random_waypoint_mobility(
            self.visual_component, 0.008, 0.02, 1000, 10000)


class MobilityModel(object):

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.n_points = 33
        self.area_max_width = 1000
        self.area_max_height = 1000
        self.all_mobility_points = []

        self.generate_distributed_random_points()

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

    def random_mobility(self, visual_component):
        """Move randomically a visual component icon on canvas.
            visual_component: A component that contains icon and node info
        """
        def move():
            # moving the device icon in canvas in random way - Rafael Sampaio
            UP = 1
            DOWN = 2
            LEFT = 3
            RIGHT = 4
            directions = [UP, DOWN, LEFT, RIGHT]
            direction = random.choice(directions)
            reference = random.randint(50, 100)

            x1 = visual_component.x
            y1 = visual_component.y
            x2 = None
            y2 = None
            tolerance = 0

            if direction == UP:
                # preventing to move out of screen canvas - Rafael Sampaio
                if not (visual_component.y - reference) < 1:
                    y2 = y1 - reference
                    x2 = x1

            elif direction == DOWN:
                # preventing to move out of screen canvas - Rafael Sampaio
                if not (visual_component.y + reference) > self.simulation_core.canvas.winfo_height():
                    y2 = y1 + reference
                    x2 = x1
                    # preventin icon cross down wall, adds icon height to prevet wall cross error - Rafael Sampaio
                    tolerance = visual_component.height

            elif direction == LEFT:
                # preventing to move out of screen canvas - Rafael Sampaio
                if not (visual_component.x - reference) < 1:
                    x2 = x1 - reference
                    y2 = y1

            elif direction == RIGHT:
                # preventing to move out of screen canvas - Rafael Sampaio
                if not (visual_component.x + reference) > self.simulation_core.canvas.winfo_width():
                    x2 = x1 + reference
                    y2 = y1
                    # preventin icon cross right wall - Rafael Sampaio
                    tolerance = visual_component.width

            if x2 and y2:
                all_coordinates_between_two_points = list(
                    bresenham(x1, y1, x2, y2))
                wall_was_found = False
                for x, y in all_coordinates_between_two_points:
                    old_x = visual_component.x
                    old_y = visual_component.y
                    if not wall_was_found:
                        # verify if object just got its destiny - Rafael Sampaio
                        if not(x == x2 and y == y2):
                            visual_component.move_on_screen(x, y)
                            if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                                # if found a collision, then rolling back to old position - Rafael Sampaio
                                visual_component.move_on_screen(
                                    old_x, old_y)
                                wall_was_found = True

        LoopingCall(move).start(0.2)

    @inlineCallbacks
    def random_waypoint_mobility(
        self,
        visual_component,
        min_speed: float,
        max_speed: float,
        min_pause: int,
        max_pause: int
    ) -> None:
        """Move randomically a visual component icon on canvas using the random waypoint mobility model.
            visual_component: A component that contains icon and node info
            min_speed: float - Min value for mobility velocility
            max_speed: float - Max value for mobility velocility
            min_pause: int - Mix pause value for a node stay at a given waypoint
            max_pause: int - Max pause value for a node stay at a given waypoint
        """
        all_coordinates_between_two_points = []
        # Choosing randomically a waypoint in all_mobility_points list - Rafael Sampaio
        next_random_point = random.choice(self.all_mobility_points)
        # Getting all coords between current node(visual_component) position and the selected next point - Rafael Sampaio
        if next_random_point:
            all_coordinates_between_two_points = list(
                bresenham(visual_component.x, visual_component.y, next_random_point['x'], next_random_point['y']))

            self.simulation_core.updateEventsCounter(
                f"Mobile Node {visual_component.deviceName} Moving to x:{next_random_point['x']} y:{next_random_point['y']} coords ")

            step_speed = random.uniform(min_speed, max_speed)
            wall_was_found = False
            tolerance = None
            for x, y in all_coordinates_between_two_points:
                old_x = visual_component.x
                old_y = visual_component.y
                # Due it is a loop, verify if last movement has resulted in a wall collision - Rafael Sampaio
                if not wall_was_found:
                    # verify if object just got its destiny - Rafael Sampaio
                    if not(x == next_random_point['x']) and not(y == next_random_point['y']):
                        # preventing icon cross wall - Rafael Sampaio
                        tolerance = 10
                        # Moving icon on screen at - Rafael Sampaio
                        visual_component.move_on_screen(x, y)
                        if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                            # if found a collision, then rolling back to old position - Rafael Sampaio
                            visual_component.move_on_screen(
                                old_x, old_y)
                            wall_was_found = True
                            break
                    yield sleep(step_speed)

            # Stay at point for a random period, so move again to another point - Rafael Sampaio
            self.simulation_core.canvas.after(random.randint(
                min_pause, max_pause), self.random_waypoint_mobility, visual_component, min_speed, max_speed, min_pause, max_pause)
