
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
        # self.allWirelessConnections = defaultdict(list)
        self.allConnections = set()
        self.allNodes = []
        self.canvas = None
        self.simulation_screen = None
        self.eventsCounter = 0
        self.allProtocols = set()
        self.project_name = None
        self.is_running = False
        self.scene_adapter = None

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

    def get_any_protocol_by_addr_and_port(self, addr, port):
        try:
            for proto in self.allProtocols:
                if proto.transport.getHost().host == addr and proto.transport.getHost().port == port:
                    return proto
        except:
            pass

    def updateEventsCounter(self, event_description):
        self.eventsCounter = self.eventsCounter + 1
        log.msg("Event: %i | " % (self.eventsCounter)+event_description)
        # Updates events counter value on screen - Rafael Sampaio
        self.simulation_screen.menubar.entryconfigure(
            4, label="Events: "+str(self.eventsCounter))

    def getConnectionById(self, id):
        try:
            filtered_list = self.allConnections[id]
            return filtered_list[0]
        except Exception as e:
            log.msg("There is no connection whith the id %i" % (id))

    def getWirelessConnectionById(self, id):
        try:
            filtered_list = self.allWirelessConnections[id]
            return filtered_list[0]
        except Exception as e:
            log.msg("There is no wireless connection whith the id %i" % (id))

    def appendConnections(self, connection):
        self.allConnections[connection.id].append(connection)

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
