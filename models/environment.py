


class Environment(object):

    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.name = None
        self.devices_list = []
        self.human_list = []
        self.x1 = 78
        self.y1 = 72
        self.x2 = 460
        self.y2 = 388
        self.limits_area = None
        self.draw_limits_area()
        
    def draw_limits_area(self) -> None:
        self.limits_area = self.simulation_core.canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2, 
            self.y2,
            fill=None,
            dash=(4,3),
            outline='red',
            width=2
        )
        
    def change_limits_area_color(self, color) -> None:
        if self.limits_area:
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                outline=color
            )