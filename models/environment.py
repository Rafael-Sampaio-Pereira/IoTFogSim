
from components.machines import Machine
from twisted.internet.task import LoopingCall

class Environment(object):

    def __init__(self, simulation_core, name, x1, y1, x2, y2):
        self.simulation_core = simulation_core
        self.name = name
        self.machine_list = []
        self.human_list = []
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.limits_area = None
        self.draw_limits_area()
        self.load_all_machines_inside_environment_area()
        LoopingCall(self.check_for_human_inside_environment_area).start(0.2)
        
    def draw_limits_area(self) -> None:
        self.limits_area = self.simulation_core.canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2, 
            self.y2,
            fill=None,
            dash=(4,3),
            outline='red',
            width=2,
            tags=("env","env_"+str(self.name))
        )

    def change_limits_area_color(self, color) -> None:
        if self.limits_area:
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                outline=color
            )

    def check_for_human_inside_environment_area(self):
        if self.limits_area:
            # get objects inside the environment area
            objects_inside_env = self.simulation_core.canvas.find_enclosed(
                self.x1, self.y1, self.x2, self.y2
            )
            qt_humans = 0
            # verify if human icon is inside the environment area
            for obj in objects_inside_env:
                if "human" in self.simulation_core.canvas.gettags(obj):
                    human = self.simulation_core.get_human_instance_by_icon_id(obj)
                    if human.current_environment != self:
                        human.current_environment = self
                    qt_humans += 1

            if qt_humans > 0:
                self.change_limits_area_color('#AAFF00')
            else:
                self.change_limits_area_color('red')


    def load_all_machines_inside_environment_area(self):
        if self.limits_area:
            # get objects inside the environment area
            objects_inside_env = self.simulation_core.canvas.find_enclosed(
                self.x1, self.y1, self.x2, self.y2
            )
            # looking for all machines inside the environment area
            for obj in objects_inside_env:
                obj = self.simulation_core.get_machine_instance_by_icon_id(obj)
                if isinstance(obj, Machine):
                    self.machine_list.append(obj)
                

            