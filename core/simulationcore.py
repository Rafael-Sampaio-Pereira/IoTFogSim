
from collections import defaultdict
import datetime
from twisted.python import log
import tkinter
from twisted.internet import tksupport
from tkinter import PhotoImage
from config.settings import version
from core.ScrollableScreen import ScrollableScreen
from importlib import import_module
from core.functions import create_csv_results_file


class SimulationCore(object):

    def __init__(self):
        self.all_links = []
        self.all_humans = []
        self.all_machines = []
        self.all_network_interfaces = []
        self.all_gateways = []
        self.all_servers = []
        self.all_apps = []
        self.all_appliances = []
        self.all_ip = []
        self.canvas = None
        self.dashboard_canvas = None
        self.simulation_screen = None
        self.dashboard_screen = None
        self.eventsCounter = 0
        self.project_name = None
        self.is_running = False
        self.scene_adapter = None
        self.global_seed = None
        self.currency_prefix = None
        self.kwh_price = None
        self.links_results = None
        self.machines_results = None
        
    def generate_results(self):
        log.msg("Info :  - | Generating simulation results...")
        
        self.machines_results = create_csv_results_file(self, "machine_results")
        machines_results_csv_header = 'name, ip, power watts, consumed energy, up time, billable amount'
        print(machines_results_csv_header, file = self.machines_results, flush=True)
        if len(self.canvas.simulation_core.all_machines) > 0:
                for machine in self.canvas.simulation_core.all_machines:
                    machine.turn_off()
                    result_line = ''
                    result_line +=machine.name+','
                    if len(machine.network_interfaces) > 0:
                        result_line += machine.network_interfaces[0].ip+','
                    else:
                        result_line += 'not connected,'
                    result_line += f'{machine.power_watts}W,'
                    result_line += machine.get_consumed_energy()+','
                    result_line += f'{str(datetime.timedelta(seconds=machine.up_time))},'
                    result_line += machine.get_billable_amount()
                    
                    print(result_line, file = self.machines_results, flush=True)
                    
        self.links_results = create_csv_results_file(self, "links_results")
        links_results_csv_header = 'name, machine 1, machine 2, delay mean, delay min, delay max, total sent packets, total dropped packets'
        print(links_results_csv_header, file = self.links_results, flush=True)
        if len(self.canvas.simulation_core.all_links) > 0:
                for link in self.canvas.simulation_core.all_links:
                    result_line = ''
                    result_line += link.name+','
                    result_line += link.network_interface_1.ip+','
                    result_line += link.network_interface_2.ip+','
                    result_line += str(round(link.get_delay_mean(),3))+'ms,'
                    result_line += str(min(link.all_delays  or [0]))+','
                    result_line += str(max(link.all_delays or [0]))+','
                    result_line += str(len(link.sent_packets))+','
                    result_line += str(len(link.dropped_packets))+','
                    
                    print(result_line, file = self.links_results, flush=True)
                    
        
        log.msg("Info :  - | Closing IoTFogSim Application...")
        
    def get_machine_by_ip(self, ip):
        # filter list by machine ip, if not found, return None
        return next(filter(lambda machine: machine.network_interfaces[0].ip == ip,  self.all_machines), None)
    
    def get_network_interface_by_ip(self, ip):
        # filter list by network_interface ip, if not found, return None
        return next(filter(lambda interface: interface.ip == ip,  self.all_network_interfaces), None)

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
            "IoTFogSim %s - An Event-Driven Network Simulator" % (version))

        # Simulation area on screen. - Rafael Sampaio
        self.simulation_screen = ScrollableScreen(
            window, self.project_name, resizeable, self)
        self.simulation_screen.pack(fill="both", expand=True)
        canvas = self.simulation_screen.getCanvas()

        self.canvas = canvas
