
import random
from twisted.internet.task import LoopingCall
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from mobility.mobility_models import MobilityModel


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
