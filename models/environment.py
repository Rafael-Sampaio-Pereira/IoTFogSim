
from apps.access_point import AccessPointApp
from apps.light_bulb import Light, LightBulbApp
from apps.router import RouterApp
from components.machines import Machine
from twisted.internet.task import LoopingCall
from PIL import ImageTk, Image
from config.settings import ICONS_PATH
from core.iconsRegister import getIconFileName

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
        self.on_light_icon = ImageTk.PhotoImage(
            file=ICONS_PATH+getIconFileName("light_on_icon")
        )
        self.off_light_icon = ImageTk.PhotoImage(
            file=ICONS_PATH+getIconFileName("light_off_icon")
        )
        self.draw_limits_area()
        self.all_lights = []
        self.load_all_machines_inside_environment_area()
        LoopingCall(self.check_for_human_inside_environment_area).start(0.2)
        
    # def load_all_lights(self):
    #     # get objects inside the environment area
    #     objects_inside_env = self.simulation_core.canvas.find_enclosed(
    #         self.x1, self.y1, self.x2, self.y2
    #     )

    #     # verify if human icon is inside the environment area
    #     for obj in objects_inside_env:
    #         if "light_bulb" in self.simulation_core.canvas.gettags(obj):
    #             print("TEM LUZ")
    #             self.all_lights.append(obj)

    def toggle_between_day_and_night(self):
        # 64799s = 17h 59m
        # 18000s = 5h
        if self.simulation_core.clock.elapsed_seconds > 64799 and self.simulation_core.clock.elapsed_seconds > 18000:
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                fill='black'
            )
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                stipple='gray50' # You can use 'gray75', 'gray50', 'gray25' and 'gray12'
            )
        else:
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                fill=''
            )
            self.simulation_core.canvas.itemconfig(
                self.limits_area,
                stipple=''
            )
        
    def draw_limits_area(self) -> None:
        self.limits_area = self.simulation_core.canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2, 
            self.y2,
            fill=None,
            dash=(4,3),
            outline='',
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
        self.toggle_between_day_and_night()
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
                    if len(self.all_lights) > 0:
                        for light in self.all_lights:
                            self.simulation_core.canvas.itemconfig(
                                light.visual_component.draggable_img,
                                image=self.on_light_icon
                            )
            

            if qt_humans > 0:
                self.change_limits_area_color('#AAFF00')
            else:
                self.change_limits_area_color('')


    def load_all_machines_inside_environment_area(self):
        if self.limits_area:
            # get objects inside the environment area
            objects_inside_env = self.simulation_core.canvas.find_enclosed(
                self.x1, self.y1, self.x2, self.y2
            )
            # looking for all machines inside the environment area
            for obj in objects_inside_env:
                obj = self.simulation_core.get_machine_instance_by_icon_id(obj)
                print(type(obj))
                if isinstance(obj, Machine) and (not isinstance(obj.app, AccessPointApp) and not isinstance(obj.app, RouterApp)):
                    self.machine_list.append(obj)
                if obj and isinstance(obj.app, Light):
                    print("TEM LUZ")
                    self.all_lights.append(obj)
