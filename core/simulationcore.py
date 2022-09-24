
from collections import defaultdict
from twisted.python import log
import tkinter
from twisted.internet import tksupport
from tkinter import PhotoImage
from config.settings import version
from core.ScrollableScreen import ScrollableScreen
from importlib import import_module


class SimulationCore(object):

    def __init__(self):
        self.all_links = set()
        self.all_machines = set()
        self.all_apps = set()
        self.all_ipv6 = set()
        self.canvas = None
        self.simulation_screen = None
        self.eventsCounter = 0
        self.project_name = None
        self.is_running = False
        self.scene_adapter = None
        
        
    def get_link_by_id(self, id):
        try:
            filtered_list = self.all_links[id]
            return filtered_list[0]
        except Exception as e:
            log.msg("There is no link whith the id %i" % (id))

    def append_link(self, link):
        self.all_links[link.id].append(link)
        
    def get_machine_by_id(self, id):
        try:
            filtered_list = self.all_machines[id]
            return filtered_list[0]
        except Exception as e:
            log.msg("There is no machine whith the id %i" % (id))

    def append_machine(self, machine):
        self.all_machines[machine.id].append(machine)
        
    def get_app_by_id(self, id):
        try:
            filtered_list = self.all_apps[id]
            return filtered_list[0]
        except Exception as e:
            log.msg("There is no app whith the id %i" % (id))

    def append_app(self, app):
        self.all_apps[app.id].append(app)




    def build_scene_adapter(self, scene_adapter_class) -> None:
        # the classPath needs to be = folder.file.class - Rafael Sampaio
        try:
            if scene_adapter_class:
                paths = scene_adapter_class.split('.')
                module_path = paths[0]+"."+paths[1]
                class_name = paths[2]
                module = import_module(module_path)
                _class = getattr(module, class_name)
                class_instance = _class(self)
                self.scene_adapter = class_instance

        except Exception as e:
            log.msg(e)

    def updateEventsCounter(self, event_description):
        self.eventsCounter = self.eventsCounter + 1
        log.msg("Event: %i | " % (self.eventsCounter)+event_description)
        # Updates events counter value on screen - Rafael Sampaio
        self.simulation_screen.menubar.entryconfigure(
            4, label="Events: "+str(self.eventsCounter))

    def create_simulation_canvas(self, resizeable):

        # These lines allows reactor suports tkinter, both runs in loop application. - Rafael Sampaio
        window = tkinter.Toplevel()
        tksupport.install(window)

        # Main window size and positions settings. - Rafael Sampaio
        w_heigth = 600
        w_width = 800
        w_top_padding = 80
        w_letf_padding = 100
        window.geometry(str(w_width)+"x"+str(w_heigth)+"+" +
                        str(w_letf_padding)+"+"+str(w_top_padding))
        if resizeable != False:
            window.attributes("-fullscreen", True)
        window.iconify()

        window.bind("<F11>", lambda event: window.attributes("-fullscreen",
                                                             not window.attributes("-fullscreen")))

        # Setting window icon. - Rafael Sampaio
        #window.tk.call('wm', 'iconphoto', window._w, PhotoImage(master=window,file='graphics/icons/iotfogsim_icon.png'))
        window.iconphoto(True, PhotoImage(
            file='graphics/icons/iotfogsim_icon.png'))

        # Setting window top text. - Rafael Sampaio
        window.title(
            "IoTFogSim %s - An Distributed Event-Driven Network Simulator" % (version))

        # Simulation area on screen. - Rafael Sampaio
        self.simulation_screen = ScrollableScreen(
            window, self.project_name, resizeable, self)
        self.simulation_screen.pack(fill="both", expand=True)
        canvas = self.simulation_screen.getCanvas()

        self.canvas = canvas

        return self.canvas
