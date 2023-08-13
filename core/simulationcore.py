
from collections import defaultdict
import datetime
from datetime import datetime as dt
from twisted.python import log
import tkinter
from twisted.internet import tksupport
from tkinter import PhotoImage
from config.settings import version
from core.ScrollableScreen import ScrollableScreen
from importlib import import_module
from core.functions import create_csv_results_file
from twisted.internet.task import LoopingCall
from tkextrafont import Font
import os
from twisted.internet import reactor

class InternalClock(object):
    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.start_time = 86399 #28800 # start clock time as seconds
        self.elapsed_seconds = self.start_time
        self.elapsed_days = 0
        self.time_speed_multiplier = 1
        self.main_loop = None
        
    def start(self):
        """Calculate elapsed time in seconds. Each seconds increases the elapsed time using the time_multiplier parameter"""
        def time_counter():
            if self.simulation_core.is_running:
                self.elapsed_seconds += 1
                self.update_clock_menu_bar()
                if self.elapsed_seconds >= 86399: # 23h 59min in seconds
                    self.elapsed_seconds=0
        self.main_loop = LoopingCall(time_counter)
        self.main_loop.start(1/self.time_speed_multiplier)
    
    def change_speed(self, new_time_speed_multiplier: int):
        if new_time_speed_multiplier != self.time_speed_multiplier:
            self.time_speed_multiplier = new_time_speed_multiplier
            self.main_loop.stop()
            self.start()
            self.update_speed_menu_label()
            
    def get_internal_time_unit(self, original_seconds):
        """Returns the time unit(i.e. one second considering the time speed multiplier"""
        return original_seconds/self.time_speed_multiplier
        
    def get_humanized_time(self):
        if self.elapsed_seconds >= 86399: # 23h 59min in seconds
            self.elapsed_days +=1
        
        return f"{self.elapsed_days} days - {str(datetime.timedelta(seconds=self.elapsed_seconds))}"
    
    def update_speed_menu_label(self):
        self.simulation_core.simulation_screen.menubar.entryconfigure(
            6, label="Speed: x"+str(self.time_speed_multiplier),)
        
    def update_clock_menu_bar(self):
        # Updates clock on screen
        self.simulation_core.simulation_screen.menubar.entryconfigure(
            5, label="Simulation clock: "+self.get_humanized_time(),)
        self.simulation_core.canvas.itemconfig(self.simulation_core.screen_clock, text=self.get_humanized_time())

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
        self.all_environments = []
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
        self.clock = None
        self.smart_hub = None
        self.output_dir =  "outputs/{:%Y_%m_%d__%H_%M_%S}".format(dt.now())
        # create results directoy if it not exist
        os.makedirs(self.output_dir, exist_ok=True)
        reactor.callInThread(self.start_clock)
        
        
    def start_clock(self):
        self.clock = InternalClock(self)
        self.clock.start()
    
    def before_close(self):
        log.msg("Info :  - | Getting ready to close the simulation...")
        self.generate_results()
        
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
                    result_line += str(machine.consumed_energy_kw)+','
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
                    result_line += str(round(link.delay_average,3))+'ms,'
                    result_line += str(link.min_delay  or [0])+','
                    result_line += str(link.max_delay or [0])+','
                    result_line += str(link.sent_packets)+','
                    result_line += str(link.dropped_packets)+','
                    
                    print(result_line, file = self.links_results, flush=True)
                    
        
        log.msg("Info :  - | Closing IoTFogSim Application...")
        log.msg(f"Info :  - | Simulation Final Clock: {self.clock.get_humanized_time()}")
        
    def get_machine_by_ip(self, ip):
        # filter list by machine ip, if not found, return None
        return next(filter(lambda machine: machine.network_interfaces[0].ip == ip if len(machine.network_interfaces)>0 else None,  self.all_machines), None)
    
    def get_network_interface_by_ip(self, ip):
        # filter list by network_interface ip, if not found, return None
        return next(filter(lambda interface: interface.ip == ip,  self.all_network_interfaces), None)

    def get_human_instance_by_icon_id(self, id):
        return next(filter(lambda human: human.visual_component.draggable_img == id,  self.all_humans), None)

    def get_machine_instance_by_icon_id(self, id):
        return next(filter(lambda obj: obj.visual_component.draggable_img == id,  self.all_machines), None)

    def build_scene_adapter(self, scene_adapter_class) -> None:
        # the classPath needs to be = folder.file.class
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
        message = "Event: %i | " % (self.eventsCounter)+event_description
        log.msg(message)
        # Updates events counter value on screen
        self.simulation_screen.menubar.entryconfigure(
            4, label="Events: "+str(self.eventsCounter))
        

    def create_simulation_canvas(self, resizeable):

        # These lines allows reactor suports tkinter, both runs in loop application.
        window = tkinter.Toplevel()
        tksupport.install(window)

        # Main window size and positions settings.
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

        # Setting window icon.
        #window.tk.call('wm', 'iconphoto', window._w, PhotoImage(master=window,file='graphics/icons/iotfogsim_icon.png'))
        window.iconphoto(True, PhotoImage(
            file='graphics/icons/iotfogsim_icon.png'))

        # Setting window top text.
        window.title(
            "IoTFogSim %s - An Event-Driven Network Simulator" % (version))

        # Simulation area on screen.
        self.simulation_screen = ScrollableScreen(
            window, self.project_name, resizeable, self)
        self.simulation_screen.pack(fill="both", expand=True)
        canvas = self.simulation_screen.getCanvas()
        font = Font(file="utils/fonts/alarm_clock.ttf", family="Alarm Clock", size=25)
        self.screen_clock = canvas.create_text((108,25), font=font, text="clock", fill='black')
        self.canvas = canvas
