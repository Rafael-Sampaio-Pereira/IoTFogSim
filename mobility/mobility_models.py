import random
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.python import log


class MobilityModel(object):

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        self.n_points = 33
        self.area_max_width = simulation_core.simulation_screen.screen_w
        self.area_max_height = simulation_core.simulation_screen.screen_h
        self.all_mobility_points = []

    def draw_points(self, point_size):
        """Draw all mobility points on canvas."""
        for point in self.all_mobility_points:
            # Drawing circles on canvas to represents every point coords
            self.simulation_core.canvas.create_oval(
                point['x'], point['y'], point['x']+point_size, point['y']+point_size, outline="red", dash=(4, 3))

    @inlineCallbacks
    def generate_area_border_points(self):
        """Distributes points of area border.
            n_points: num of points to be distributed into a given area
            area_max_width: max width of desired area
            area_max_height: max height of desired area
        """
        log.msg("Info : - | Generating area borde for mobility points...")
        # waiting for mobility model object get the simulation core
        yield sleep(0.5)
        point_size = 1
        left_padding = 80
        top_padding = 80

        # generating top line points
        for x in range(left_padding, self.area_max_width):
            # top line position
            y = top_padding
            self.all_mobility_points.append({"x": x, "y": y})

        # generating bottom line points
        for x in range(left_padding, self.area_max_width):
            # bottom line position
            y = self.area_max_height
            self.all_mobility_points.append({"x": x, "y": y})

        # generating left line points
        for y in range(top_padding, self.area_max_height):
            # left line position
            x = left_padding
            self.all_mobility_points.append({"x": x, "y": y})

        # generating rigth line points
        for y in range(top_padding, self.area_max_height):
            # left line position
            x = self.area_max_width
            self.all_mobility_points.append({"x": x, "y": y})

        # Drawing points in canvas
        self.draw_points(point_size)

    @inlineCallbacks
    def generate_distributed_random_points(self):
        """Distributes points using uniform distribution.
            n_points: num of points to be distributed into a given area
            area_max_width: max width of desired area
            area_max_height: max height of desired area
        """
        log.msg("Info : - | Generating mobility points...")
        # waiting for mobility model object get the simulation core
        yield sleep(0.5)
        point_size = 20
        left_padding = 100
        top_padding = 100
        for point in range(1, self.n_points+1):
            # Casting to int due uniform distribution returns float
            x = int(random.uniform(left_padding, self.area_max_width-100))
            y = int(random.uniform(top_padding, self.area_max_height-100))

            if self.simulation_core.scene_adapter and self.simulation_core.scene_adapter.ground_plan:
                # Avoiding to place points into walls
                if self.simulation_core.scene_adapter.ground_plan.verify_wall_collision(x, y, tolerance=point_size):
                    x += point_size+self.simulation_core.scene_adapter.ground_plan.wall_tickness
                    y += point_size+self.simulation_core.scene_adapter.ground_plan.wall_tickness

            self.all_mobility_points.append({"x": x, "y": y})
        # Drawing points in canvas
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
