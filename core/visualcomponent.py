import tkinter
from config.settings import ICONS_PATH

from twisted.python import log
from PIL import ImageTk, Image


class VisualComponent(object):

    def __init__(self, is_wireless, simulation_core, name, file, x, y, coverage_area_radius, device):
        self.simulation_core = simulation_core
        self.x = x
        self.y = y
        self.move_flag = False
        self.name = name
        self.draggable_signal_circle = None
        self.coverage_area_radius = coverage_area_radius
        self.signal_radius = None

        # this refers to the equivalente device of this visual component - Rafael Sampaio
        # By using the 'device' atribute, is possible access any atibute of the device instance, such as application - Rafael Sampaio
        self.device = device

        self.is_wireless = is_wireless

        if self.is_wireless:
            self.signal_radius = 1
            self.coverage_area_radius = coverage_area_radius
            # The signal circle object to show wifi coverage area. - Rafael Sampaio
            # coverage are need not to be visible. - Rafael Sampaio
            self.draggable_coverage_area_circle = self.simulation_core.canvas.create_oval(
                self.x+self.coverage_area_radius, self.y+self.coverage_area_radius, self.x-self.coverage_area_radius, self.y-self.coverage_area_radius, fill="", outline="", width=1, stipple="gray12")

            # The signal circle object starts with no fill and no outline colors, these colors will be set in the propagate_signal method. - Rafael Sampaio
            self.draggable_signal_circle = self.simulation_core.canvas.create_oval(
                self.x, self.y, self.x, self.y, fill="", outline="", dash=(4, 3), tag="wireless_signal")

            simulation_core.canvas.tag_bind(
                self.draggable_coverage_area_circle, '<Button1-Motion>', self.move)
            simulation_core.canvas.tag_bind(
                self.draggable_coverage_area_circle, '<ButtonRelease-1>', self.release)
            simulation_core.canvas.tag_bind(
                self.draggable_signal_circle, '<Button1-Motion>', self.move)
            simulation_core.canvas.tag_bind(
                self.draggable_signal_circle, '<ButtonRelease-1>', self.release)

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

            if self.is_wireless:
                self.simulation_core.canvas.move(self.draggable_coverage_area_circle,
                                                 new_xpos-self.mouse_xpos, new_ypos-self.mouse_ypos)

                self.simulation_core.canvas.move(self.draggable_signal_circle,
                                                 new_xpos-self.mouse_xpos, new_ypos-self.mouse_ypos)

            self.simulation_core.canvas.move(self.draggable_name,
                                             new_xpos-self.mouse_xpos, new_ypos-self.mouse_ypos)

            self.simulation_core.canvas.move(self.draggable_alert,
                                             new_xpos-self.mouse_xpos, new_ypos-self.mouse_ypos)

            self.simulation_core.canvas.move(self.draggable_img,
                                             new_xpos-self.mouse_xpos, new_ypos-self.mouse_ypos)

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            if self.is_wireless:
                self.simulation_core.canvas.tag_raise(
                    self.draggable_coverage_area_circle)
                self.simulation_core.canvas.tag_raise(
                    self.draggable_signal_circle)
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
        if self.is_wireless:
            self.simulation_core.canvas.moveto(
                self.draggable_coverage_area_circle,
                x, y
            )
            self.simulation_core.canvas.moveto(
                self.draggable_signal_circle,
                x, y
            )

        self.simulation_core.canvas.moveto(
            self.draggable_name,
            x-10, y-15
        )
        self.simulation_core.canvas.moveto(
            self.draggable_alert,
            x, y
        )
        self.simulation_core.canvas.moveto(
            self.draggable_img,
            x, y
        )
