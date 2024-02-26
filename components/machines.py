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
import os
from datetime import datetime
import random

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
        self.app.simulation_core = simulation_core
        self.app.machine = self
        self.is_turned_on = False
        self.power_watts = power_watts
        self.up_time = 0 # expressed in seconds
        self.calculating_up_time = False
        self.power_float_margin = 0.7
        self.consumed_energy_kwh = 0
        self.current_consumption = 0
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert,fill='red')
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert,font=('Helvetica', 10, 'bold'))
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text='⏻')
        
    def simulate_power_consumption(self):
        """ This simulates power consumption considering power variance.
        To call it, you need to use a variance margin(float_margin) value"""
        min_power = None
        if self.power_watts - self.power_float_margin < 1:
            min_power = self.power_watts
        else:
            min_power = self.power_watts - self.power_float_margin
            
        max_power = self.power_watts+self.power_float_margin
        if self.simulation_core.global_seed:
                random.seed(self.simulation_core.global_seed)
        final_value = random.uniform(min_power, max_power)

        # print(f"name: {self.name}, original: {self.power_watts}, max: {max_power}, min: {min_power}, final: {final_value}")

        return final_value
        
                        
    def get_billable_amount(self):
        return self.simulation_core.currency_prefix+" "+str(
            round(float(self.consumed_energy_kwh)*self.simulation_core.kwh_price,3)
        )
        
    # def get_consumed_energy(self):
    #     """
    #         https://www.youtube.com/watch?v=U9Tm7Bmr-i4
    #     """
    #     base_second = 0.000277778 # 1 second means 0,000277778 hour
    #     active_hours = base_second * self.up_time
    #     kw = self.simulate_power_consumption()/1000
    #     consumed_energy = str(round((kw * active_hours),5))+" Kwh"
    #     return consumed_energy
    
    def calculate_consumed_energy(self):
        """
            https://www.youtube.com/watch?v=U9Tm7Bmr-i4
        """
        base_second = 0.000277778 # 1 second means 0,000277778 hour
        # active_hours = base_second * self.up_time
        active_hours = self.up_time / 3600
        self.current_consumption = self.simulate_power_consumption()/1000
        self.consumed_energy_kwh = round((self.current_consumption * active_hours),2)
        

    def calculate_up_time(self):
        """Calculate active time in seconds. Each seconds increases the active time"""
        def time_counter():
            if self.is_turned_on:
                self.up_time += 1
                self.calculate_consumed_energy()
                            
        LoopingCall(time_counter).start(self.simulation_core.clock.get_internal_time_unit(1))
        self.calculating_up_time = True
        
    def colorize_signal(self, color='red'):
        # setting the color of signal(circle border) from transparent to red.
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline=color)
        
    @inlineCallbacks
    def propagate_signal(self):
        if self.simulation_core.clock.time_speed_multiplier <= 10:
            for n in range(0, self.visual_component.coverage_area_radius):
                # The circle signal starts with raio 1 and propagates to raio 100.
                if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
                    # the ssignal radius propagates at 1 units per time.
                    self.visual_component.signal_radius += 10
                    
                else:
                    # Cleaning propagated signal for restore the signal draw.
                    self.visual_component.signal_radius = -1
                    
                self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y +
                                                    self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)

                yield sleep(self.simulation_core.clock.get_internal_time_unit(0.005))
            self.visual_component.signal_radius = 1
        
        
    def turn_on(self, event=None):
        if not self.is_turned_on:
            self.is_turned_on = True
            if not self.calculating_up_time:
                reactor.callFromThread(self.calculate_up_time)
            self.simulation_core.updateEventsCounter(f"{self.name} - Turning on {self.type}...")
            if len(self.network_interfaces)>0:
                self.update_name_on_screen(self.name+'\n'+self.network_interfaces[0].ip)
            else:
                self.update_name_on_screen(self.name)

            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert,fill='green')
            # self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text='ON')
            
            if self.is_wireless:
                self.colorize_signal()
            reactor.callFromThread(self.app.start)
        
    def turn_off(self, event=None):
        self.is_turned_on = False
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert,fill='red')
        self.simulation_core.updateEventsCounter(f"{self.name} - Turning off {self.type}...")
                
    def verify_if_connection_link_already_exists(self, machine):
        """Verify if connection link already exists, if exists returns it"""
        return next(filter(lambda link: link.network_interface_1.machine == machine or link.network_interface_2.machine == machine,  self.links), None)
    
    def update_name_on_screen(self, msg):
        if msg:
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(msg))
            
    def toggle_power_state(self):
        if self.is_turned_on:
            self.turn_off()
        else:
            self.turn_on()
