
from apps.access_point import AccessPointApp
from apps.light_bulb import Light
from apps.router import RouterApp
from apps.smart_hub import SmartHubApp
from components.machines import Machine
from twisted.internet.task import LoopingCall
from PIL import ImageTk, Image
from twisted.internet import reactor
from config.settings import ICONS_PATH
from core.iconsRegister import getIconFileName

class Environment(object):

    def __init__(self, simulation_core, name, type, x1, y1, x2, y2):
        self.simulation_core = simulation_core
        self.name = name
        self.type = type
        self.machine_list = []
        self.human_list = []
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.limits_area = None
        self.sensor_x = (x1+x2)/2
        self.sensor_y = (y1+y2)/2
        self.occupancy_sensor = Machine(
            simulation_core,
            self.name+'_occupancy_sensor',
            0,
            'sensor_icon',
            True,
            self.sensor_x,
            self.sensor_y,
            'apps.occupancy_sensor.OccupancySensorApp',
            'Sensor',
            100,
            0.5
        )
        self.occupancy_sensor.app.environment = self
        simulation_core.all_machines.append(self.occupancy_sensor)
        self.on_light_icon = ImageTk.PhotoImage(
            file=ICONS_PATH+getIconFileName("light_on_icon")
        )
        self.off_light_icon = ImageTk.PhotoImage(
            file=ICONS_PATH+getIconFileName("light_off_icon")
        )
        self.draw_limits_area()
        self.all_lights = []
        self.load_all_machines_inside_environment_area()
        reactor.callLater(0.1, self.occupancy_sensor.turn_on)
        LoopingCall(self.check_for_human_inside_environment_area).start(
            self.simulation_core.clock.get_internal_time_unit(0.4))
        reactor.callLater(0.7,self.occupancy_sensor.colorize_signal, '#AAFF00')
        
        

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
        if self.limits_area:
            # get objects inside the environment area
            objects_inside_env = self.simulation_core.canvas.find_enclosed(
                self.x1, self.y1, self.x2, self.y2
            )
            qt_humans = 0
            human = None
            # verify if human icon is inside the environment area
            for obj in objects_inside_env:
                if "human" in self.simulation_core.canvas.gettags(obj):
                    human = self.simulation_core.get_human_instance_by_icon_id(obj)
                    if human.current_environment != self:
                        human.current_environment = self
                    qt_humans += 1

            if qt_humans > 0:
                self.occupancy_sensor.app.occupancy_sensing.occupancy = 'OCCUPIED'
                self.occupancy_sensor.propagate_signal()
                self.change_limits_area_color('#AAFF00')
                self.occupancy_sensor.app.last_actor = human.name
            else:
                self.occupancy_sensor.app.occupancy_sensing.occupancy = 'UNOCCUPIED'
                self.change_limits_area_color('')
                self.occupancy_sensor.app.last_actor = 'Automation System'

            if len(self.all_lights) > 0:
                if qt_humans > 0:
                    # 64799s = 17h 59m
                    # 18000s = 5h
                    # convert time to seconds at https://onlinetimetools.com/convert-time-to-seconds
                    self.simulation_core.canvas.itemconfig(
                        self.limits_area,
                        fill=''
                    )
                    self.simulation_core.canvas.itemconfig(
                        self.limits_area,
                        stipple=''
                    )
                    if self.simulation_core.clock.elapsed_seconds > 64799:
                        for light in self.all_lights:
                            self.simulation_core.canvas.itemconfig(
                                light.visual_component.draggable_img,
                                image=self.on_light_icon
                            )
                            if not light.is_turned_on:
                                light.turn_on()
                                light.app.last_actor = human.name
                                
                    elif self.simulation_core.clock.elapsed_seconds < 18000:
                        for light in self.all_lights:
                            self.simulation_core.canvas.itemconfig(
                                light.visual_component.draggable_img,
                                image=self.on_light_icon
                            )
                            if not light.is_turned_on:
                                light.turn_on()
                                light.app.last_actor = human.name
                    else:
                        for light in self.all_lights:
                            self.simulation_core.canvas.itemconfig(
                                light.visual_component.draggable_img,
                                image=self.off_light_icon
                            )
                            if light.is_turned_on:
                                light.turn_off()
                                light.app.last_actor = 'Automation System'
                    
                else:
                    # 64799s = 17h 59m
                    # 18000s = 5h
                    if self.simulation_core.clock.elapsed_seconds > 64799:
                        self.simulation_core.canvas.itemconfig(
                            self.limits_area,
                            fill='black'
                        )
                        self.simulation_core.canvas.itemconfig(
                            self.limits_area,
                            stipple='gray50' # You can use 'gray75', 'gray50', 'gray25' and 'gray12'
                        )
                    elif self.simulation_core.clock.elapsed_seconds < 18000:
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
                    
                    for light in self.all_lights:
                        self.simulation_core.canvas.itemconfig(
                            light.visual_component.draggable_img,
                            image=self.off_light_icon
                        )
                        if light.is_turned_on:
                            light.turn_off()
                            light.app.last_actor = 'Automation System'


    def load_all_machines_inside_environment_area(self):
        if self.limits_area:
            # get objects inside the environment area
            objects_inside_env = self.simulation_core.canvas.find_enclosed(
                self.x1, self.y1, self.x2, self.y2
            )
            # looking for all machines inside the environment area
            for obj in objects_inside_env:
                obj = self.simulation_core.get_machine_instance_by_icon_id(obj)
                if isinstance(obj, Machine) and (not isinstance(obj.app, AccessPointApp) and not isinstance(obj.app, RouterApp) and not isinstance(obj.app, SmartHubApp)):
                    self.machine_list.append(obj)
                if obj and isinstance(obj.app, Light):
                    self.all_lights.append(obj)
