
import random
from twisted.internet.task import LoopingCall
from bresenham import bresenham
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from mobility.mobility_models import MobilityModel

"""
Random Walk Model
As a variant of RWP, RW is also an important random mobility model. The node in RW randomly selects
a direction from [0, 2π], from [Vmin, Vmax] Randomly select a speed, and then move to a new 
position according to the selected direction and speed. In the process of node movement, select a 
time interval t or a fixed distance d. When the node moves for t time or d length, reselect the 
direction and speed of the node. 

found at: https://www.big-meter.com/opensource/en/5ff4abd139fb6523f2624e91.html
"""


class RandomWalkMobility(MobilityModel):
    """Move randomically a visual component icon on canvas.
        visual_component: A component that contains icon and node info
        step_distance: Number of pixels to move at each step
    """

    def __init__(self, visual_component, simulation_core, step_distance):
        super().__init__(simulation_core)
        self.simulation_core = simulation_core
        self.visual_component = visual_component
        self.step_distance = step_distance
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

        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = None
        y2 = None
        tolerance = 0

        if direction == UP:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.y - self.step_distance) < 1:
                y2 = y1 - self.step_distance
                x2 = x1

        elif direction == DOWN:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.y + self.step_distance) > self.simulation_core.canvas.winfo_height():
                y2 = y1 + self.step_distance
                x2 = x1
                # preventin icon cross down wall, adds icon height to prevet wall cross error - Rafael Sampaio
                tolerance = self.visual_component.height

        elif direction == LEFT:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.x - self.step_distance) < 1:
                x2 = x1 - self.step_distance
                y2 = y1

        elif direction == RIGHT:
            # preventing to move out of screen canvas - Rafael Sampaio
            if not (self.visual_component.x + self.step_distance) > self.simulation_core.canvas.winfo_width():
                x2 = x1 + self.step_distance
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
                        if self.simulation_core.scene_adapter and self.simulation_core.scene_adapter.ground_plan:
                            if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance):
                                # if found a collision, then rolling back to old position - Rafael Sampaio
                                self.visual_component.move_on_screen(
                                    old_x, old_y)
                                wall_was_found = True
