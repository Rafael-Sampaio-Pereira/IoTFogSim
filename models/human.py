
import uuid
from core.visualcomponent import VisualComponent
import tkinter
from config.settings import ICONS_PATH
from mobility.random_direction_mobility import RandomDirectionMobility
from mobility.random_walk_mobility import RandomWalkMobility
from mobility.random_waypoint_mobility import RandomWaypointMobility
from twisted.python import log
from PIL import ImageTk, Image
from core.iconsRegister import getIconFileName
from mobility.graph_random_waypoint_mobility import GraphRandomWaypointMobility


class Human(object):
    def __init__(self, simulation_core, name, age, weight, height, icon, x, y, mobility_model_class=None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.x = x
        self.y = y
        self.simulation_core = simulation_core
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file
        self.visual_component = HumanVisualComponent(
            self.simulation_core,
            self.name, self.icon, x, y)
        self.simulation_core.updateEventsCounter(f"{self.name} - Initializing human...")

    def start(self):
        self.run_mobility()

    def run_mobility(self):
        # GraphRandomWaypointMobility(
        #     self.visual_component,
        #     self.simulation_core,
        #     0.02,
        #     0.08,
        #     2,
        #     10
        # )
        
        # RandomDirectionMobility(
        #     self.visual_component,
        #     self.simulation_core,
        #     0.02,
        #     0.08,
        #     2,
        #     10
        # )

        # RandomWalkMobility(
        #     self.visual_component,
        #     self.simulation_core,
        #     10
        # )
        
        RandomWaypointMobility(
            self.visual_component,
            self.simulation_core,
            0.02,
            0.08,
            2,
            10
        )

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
            x, y, image=self.image_file, tag="icon")

        self.draggable_name = self.simulation_core.canvas.create_text(x, y+22, fill="black", font="Arial 7",
                                                                      text=name)

        self.draggable_alert = self.simulation_core.canvas.create_text(x, y-22, fill="black", font="Times 7",
                                                                       text="")
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
        
