from typing_extensions import Self
import uuid
from core.functions import import_and_instantiate_class_from_string
from config.settings import ICONS_PATH
from core.visualcomponent import VisualComponent
from core.iconsRegister import getIconFileName
from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from core.functions import sleep
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


class Machine(object):
    def __init__(
            self,
            simulation_core,
            name,
            MIPS,
            icon,
            is_wireless,
            x,
            y,
            app,
            type,
            coverage_area_radius,
            connected_gateway_addrs,
            power_watts
        ):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.MIPS = MIPS
        icon_file = getIconFileName(icon)
        self.icon = ICONS_PATH+icon_file
        self.is_wireless = is_wireless
        self.type = type
        self.app = import_and_instantiate_class_from_string(app)
        self.network_interfaces = []
        self.visual_component = VisualComponent(
            self.is_wireless,
            self.simulation_core,
            self.name, self.icon, x, y, coverage_area_radius, self)
        self.peers = []
        self.links = []
        self.connected_gateway_addrs = connected_gateway_addrs
        self.app.simulation_core = simulation_core
        self.app.machine = self
        self.is_turned_on = False
        self.power_watts = power_watts
        self.up_time = 0 # expressed in seconds
                
    def get_billable_amount(self):
        return self.simulation_core.currency_prefix+" "+str(round(float(self.get_consumed_energy()[:-4])*self.simulation_core.kwh_price,3))
        
    def get_consumed_energy(self):
        """
            https://www.youtube.com/watch?v=U9Tm7Bmr-i4
        """
        base_second = 0.000277778 # 1 second means 0,000277778 hour
        active_hours = base_second * self.up_time
        kw = self.power_watts/1000
        consumed_energy = str(round((kw * active_hours),5))+" Kwh"
        return consumed_energy
        
    def calculate_up_time(self):
        """Calculate active time in seconds. Each seconds increases the active time"""
        def time_conter():
            if self.is_turned_on:
                self.up_time += 1
        LoopingCall(time_conter).start(2)
    
    @inlineCallbacks
    def propagate_signal(self):
        # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline="red")

        for n in range(0, self.visual_component.coverage_area_radius):
            # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
            if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
                # the ssignal radius propagates at 1 units per time. - Rafael Sampaio
                self.visual_component.signal_radius += 2
                self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y +
                                                   self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
            else:
                # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
                self.simulation_core.canvas.itemconfig(
                    self.visual_component.draggable_signal_circle, outline="")
                self.visual_component.signal_radius = 1
                self.simulation_core.canvas.update()
            yield sleep(0.001)
        
    def turn_on(self, event=None):
        if not self.is_turned_on:
            self.is_turned_on = True
            reactor.callFromThread(self.calculate_up_time)
            self.simulation_core.updateEventsCounter(f"{self.name} - Turning on {self.type}...")
            self.update_name_on_screen(self.name+'\n'+self.network_interfaces[0].ip)
            reactor.callFromThread(self.app.start)
        
    def turn_off(self, event=None):
        self.is_turned_on = False
        self.simulation_core.updateEventsCounter(f"{self.name} - Turning off {self.type}...")
                
    def verify_if_connection_link_already_exists(self, machine):
        """Verify if connection link already exists, if exists returns it"""
        return next(filter(lambda link: link.network_interface_1.machine == machine or link.network_interface_2.machine == machine,  self.links), None)
    
    def update_name_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(msg))
