
import uuid
from core.functions import import_and_instantiate_class_from_string, import_and_instantiate_class_from_string_with_params
from core.visualcomponent import VisualComponent
from config.settings import ICONS_PATH
from mobility.random_direction_mobility import RandomDirectionMobility
from mobility.random_walk_mobility import RandomWalkMobility
from mobility.random_waypoint_mobility import RandomWaypointMobility
from twisted.python import log
from PIL import ImageTk, Image
from core.iconsRegister import getIconFileName
from mobility.graph_random_waypoint_mobility import GraphRandomWaypointMobility
from twisted.internet.task import LoopingCall

from models.behavior import BasicBehavior, TimeDrivenBehavior

class Human(object):
    def __init__(self, simulation_core, name, age, weight, height, icon, x, y, behavior, mobility_model_class=None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.x = x
        self.y = y
        self.current_environment = None
        self.last_environment = None
        self.simulation_core = simulation_core
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file
        self.visual_component = HumanVisualComponent(
            self.simulation_core,
            self.name, self.icon, x, y)
        self.simulation_core.updateEventsCounter(f"{self.name} - Initializing human...")
        self.mobility = None
        # self.behavior = None
        self.behavior = import_and_instantiate_class_from_string_with_params(behavior, *[self])
        self.state = 'AWAKE'

    def set_state(self, new_state):
        self.state = new_state

    def start(self):
        # self.behavior = TimeDrivenBehavior(self)
        
        self.behavior.run()

    def is_at_bed(self):
        bed = next(filter(
                lambda point: point["name"] == 'BED',
                self.mobility.all_mobility_points), None)
        if bed:
            if self.visual_component.x == bed['x'] and self.visual_component.y == bed['y']:
                return True
        return False
            
    def check_current_environment(self):
        if self.current_environment:
            
            human = self.visual_component.draggable_img
            human = self.simulation_core.canvas.bbox(human)

            # We compute the center of the person:
            human_xcenter = (human[0]+human[2])/2
            human_ycenter = (human[1]+human[3])/2
            
            env = self.current_environment.limits_area           
            env = self.simulation_core.canvas.bbox(env)
            
            # First we make sure we compare things in the right order
            # You can skip that part if you are sure that in all cases x1 < x2 and y1 < y2
            env_xmin = min(env[0], env[2])
            env_xmax = max(env[0], env[2])
            env_ymin = min(env[1], env[3])
            env_ymax = max(env[1], env[3])

            # Then you perform your checks.

            in_range_along_x = human_xcenter < env_xmax and env_xmin < human_xcenter
            in_range_along_y = human_ycenter < env_ymax and env_ymin < human_ycenter

            # verify if human is into env range
            if in_range_along_x and in_range_along_y:
                pass
            else:
                self.current_environment = None


    # def run_mobility(self):

    #     # self.mobility = GraphRandomWaypointMobility(
    #     #     self.visual_component,
    #     #     self.simulation_core,
    #     #     0.02,
    #     #     0.08,
    #     #     2,
    #     #     10
    #     # )
        
    #     # self.mobility = RandomDirectionMobility(
    #     #     self.visual_component,
    #     #     self.simulation_core,
    #     #     0.02,
    #     #     0.08,
    #     #     2,
    #     #     10
    #     # )

    #     # self.mobility = RandomWalkMobility(
    #     #     self.visual_component,
    #     #     self.simulation_core,
    #     #     10
    #     # )
        
    #     # self.mobility = RandomWaypointMobility(
    #     #     self.visual_component,
    #     #     self.simulation_core,
    #     #     0.02,
    #     #     0.08,
    #     #     2,
    #     #     10
    #     # )

    #     self.mobility.is_stopped = False
        
class HumanVisualComponent(object):

    def __init__(self, simulation_core, name, file, x, y):
        self.simulation_core = simulation_core
        self.x = x
        self.y = y
        self.move_flag = False
        self.name = name
        self.mouse_xpos = None
        self.mouse_ypos = None

        self.image_file = ImageTk.PhotoImage(file=file)
        self.height = self.image_file.height()
        self.width = self.image_file.width()
        self.draggable_img = self.simulation_core.canvas.create_image(
            x, y, image=self.image_file, tags=("icon", "human", "human_"+str(self.name)))

        self.draggable_name = self.simulation_core.canvas.create_text(
            x, y+22, fill="black", font="Arial 7", text=name)

        self.draggable_alert = self.simulation_core.canvas.create_text(
            x, y-22, fill="black", font="Times 7", text="")
        # font="Times 9 italic bold"

        simulation_core.canvas.tag_bind(
            self.draggable_alert, '<Button1-Motion>', self.move)
        simulation_core.canvas.tag_bind(
            self.draggable_alert, '<ButtonRelease-1>', self.release)
        simulation_core.canvas.tag_bind(
            self.draggable_name, '<Button1-Motion>', self.move)
        simulation_core.canvas.tag_bind(
            self.draggable_name, '<ButtonRelease-1>', self.release)
        simulation_core.canvas.tag_bind(
            self.draggable_img, '<Button1-Motion>', self.move)
        simulation_core.canvas.tag_bind(
            self.draggable_img, '<ButtonRelease-1>', self.release)
        simulation_core.canvas.configure(cursor="hand1")
        self.move_flag = False

    def move(self, event):

        if self.move_flag:
            new_xpos = event.x
            new_ypos = event.y
            self.x = new_xpos
            self.y = new_ypos

            self.simulation_core.canvas.move(
                self.draggable_name,
                new_xpos-self.mouse_xpos,
                new_ypos-self.mouse_ypos
            )

            self.simulation_core.canvas.move(
                self.draggable_alert,
                new_xpos-self.mouse_xpos,
                new_ypos-self.mouse_ypos
            )

            self.simulation_core.canvas.move(
                self.draggable_img,
                new_xpos-self.mouse_xpos,
                new_ypos-self.mouse_ypos
            )

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.simulation_core.canvas.tag_raise(self.draggable_img)
            self.simulation_core.canvas.tag_raise(self.draggable_name)
            self.simulation_core.canvas.tag_raise(self.draggable_alert)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False

    def set_coverage_area_radius(self, radius):
        self.coverage_area_radius = radius

    def move_on_screen(self, x, y):
        self.x = x
        self.y = y

        # self.simulation_core.canvas.moveto(
        #     self.draggable_name,
        #     x-10, y-15
        # )
        # self.simulation_core.canvas.moveto(
        #     self.draggable_alert,
        #     x, y
        # )
        # self.simulation_core.canvas.moveto(
        #     self.draggable_img,
        #     x, y
        # )

        self.simulation_core.canvas.coords(self.draggable_name, x-10, y-15)
        self.simulation_core.canvas.coords(self.draggable_alert, x, y)
        self.simulation_core.canvas.coords(self.draggable_img, x, y)
        