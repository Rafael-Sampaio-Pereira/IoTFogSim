from tkinter import RIGHT
from applications.mobilityapp import MobileProducerApp
import random
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from bresenham import bresenham


class SmartHomeAdapter(object):
    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.ground_plan = SimpleGroundPlan(simulation_core)


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
        self.simulation_core.canvas.itemconfig(wall, fill="#141313")
        reactor.callLater(
            0.7, self.simulation_core.canvas.itemconfig, wall, fill=original_color)

    def verify_wall_collision(self, x, y, tolerance=0):
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
        self.random_mobility()

    def random_mobility(self):
        def move():
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
                # preventing to move out of screen canvas
                if not (self.visual_component.y - reference) < 1:
                    y2 = y1 - reference
                    x2 = x1

            elif direction == DOWN:
                # preventing to move out of screen canvas
                if not (self.visual_component.y + reference) > self.simulation_core.canvas.winfo_height():
                    y2 = y1 + reference
                    x2 = x1
                    # preventin icon cross down wall, adds icon height to prevet wall cross error
                    tolerance = self.visual_component.height

            elif direction == LEFT:
                # preventing to move out of screen canvas
                if not (self.visual_component.x - reference) < 1:
                    x2 = x1 - reference
                    y2 = y1

            elif direction == RIGHT:
                # preventing to move out of screen canvas
                if not (self.visual_component.x + reference) > self.simulation_core.canvas.winfo_width():
                    x2 = x1 + reference
                    y2 = y1
                    # preventin icon cross right wall
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
                                # if found a collision, then rolling back to old position
                                self.visual_component.move_on_screen(
                                    old_x, old_y)
                                wall_was_found = True

        LoopingCall(move).start(0.2)
