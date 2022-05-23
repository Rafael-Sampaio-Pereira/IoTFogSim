from applications.mobilityapp import MobileProducerApp
import random
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


class SmartHomeAdapter(object):
    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.ground_plan = SimpleGroundPlan(simulation_core)


class SimpleGroundPlan(object):
    """Ground Plan for simulate house envirioment in smart home context."""

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.wall_tickness = 10
        self.wall_color = "gray"

        self.draw_wall(50, 100, 1000, "v")
        self.draw_wall(600, 100, 350, "v")
        self.draw_wall(1000, 100, 1010, "v")

        self.draw_wall(60, 100, 800, "h")
        self.draw_wall(50, 500, 600, "h")
        self.draw_wall(50, 700, 600, "h")
        self.draw_wall(50, 1000, 1010, "h")

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
        self.run_random_mobility()

    def verify_wall_collision(self):
        def blink_wall(wall):
            original_color = self.simulation_core.scene_adapter.ground_plan.wall_color
            self.simulation_core.canvas.itemconfig(wall, fill="red")
            reactor.callLater(
                0.7, self.simulation_core.canvas.itemconfig, wall, fill=original_color)

        # finding all the wifi devices on the canvas screen. - Rafael Sampaio
        all_wall = self.simulation_core.canvas.find_withtag("wall")
        collision_items = self.simulation_core.canvas.find_overlapping(
            self.visual_component.x, self.visual_component.y, self.visual_component.x, self.visual_component.y)

        for wall in all_wall:
            if wall in collision_items:
                blink_wall(wall)

    # @override

    def run_random_mobility(self):
        def move():
            # moving the device icon in canvas in random way - Rafael Sampaio
            direction = random.randint(1, 4)
            reference = random.randint(1, 100)

            if direction == 1:  # up
                if not (self.visual_component.y - reference) < 1:
                    self.visual_component.y = self.visual_component.y - reference
                    self.verify_wall_collision()
            elif direction == 2:  # down
                if not (self.visual_component.y + reference) > self.simulation_core.canvas.winfo_height():
                    self.visual_component.y = self.visual_component.y + reference
                    self.verify_wall_collision()
            elif direction == 3:  # left
                if not (self.visual_component.x - reference) < 1:
                    self.visual_component.x = self.visual_component.x - reference
                    self.verify_wall_collision()
            elif direction == 4:  # right
                if not (self.visual_component.x + reference) > self.simulation_core.canvas.winfo_width():
                    self.visual_component.x = self.visual_component.x + reference
                    self.verify_wall_collision()

            if self.visual_component.is_wireless:
                self.simulation_core.canvas.moveto(self.visual_component.draggable_coverage_area_circle,
                                                   self.visual_component.x, self.visual_component.y)

                self.simulation_core.canvas.moveto(self.visual_component.draggable_signal_circle,
                                                   self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_name,
                                               self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_alert,
                                               self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_img,
                                               self.visual_component.x, self.visual_component.y)

        LoopingCall(move).start(0.1)
