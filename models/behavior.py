from typing import Any
from twisted.internet.task import LoopingCall
import random
from twisted.internet import reactor
from apps.air_conditioner import AirConditionerApp
from apps.refrigerator import RefrigeratorApp
from apps.shower import ShowerApp
from apps.smart_hub import Scene
from apps.smart_tv import SmartTvApp
from apps.vacuum_bot import VacuumBotApp
from apps.ventilator import VentilatorApp
from core.functions import readable_time_to_seconds

from mobility.probabilistic_graph_random_waypoint_mobility import ProbabilisticGraphRandomWaypointMobility

smarttv_functions = [
    'turn_on',
    'turn_off',
    'set_channel',
    'set_volume',
    'set_source'
]
vaccumbot_functions = [
    'turn_on',
    'turn_off',
]
shower_functions = [
    'turn_on',
    'turn_off',
    'set_temperature'
]
refrigerator_functions = [
    'turn_on',
    'turn_off',
    'set_temperature'
]
air_conditioner_functions = [
    'turn_on',
    'turn_off',
    'set_temperature',
    'set_fan_speed'
]
ventilator_functions = [
    'turn_on',
    'turn_off',
    'set_fan_speed'
]

class BasicBehavior(object):
    def __init__(self, human):
        self.human = human
        self.period = None
    
    def go_to_point_and_stay_at(self, point_name, state_before, state_after, duration):
        self.human.mobility.set_next_mobility_point(point_name)
        reactor.callLater(
            self.human.simulation_core.clock.get_internal_time_unit(20),
            self.human.set_state,
            state_before
        )
        reactor.callLater(
            self.human.simulation_core.clock.get_internal_time_unit(duration),
            self.human.set_state,
            state_after
        )

    def interact_to_current_environment_machines_weighted_choices(self):
        """Chooses randomicly a machine in the environment
            to interact to, then it can choose a machine
            function based on weighted choices options and day period."""
        
        if self.human.current_environment:
            # if self.simulation_core.global_seed:
            #     random.seed(self.simulation_core.global_seed)
            
            if len(self.human.current_environment.machine_list) > 0:
                
                random.shuffle(self.human.current_environment.machine_list)
                # Select a machine randomly from environment machines list
                selected_machine = random.choice(self.human.current_environment.machine_list)
                selected_function = None
                choices_functions = []
                weights = ()

                if selected_machine:
                    if self.period == 'morning':
                        choices_functions, weights = self.morning_actions(selected_machine)
                    
                    elif self.period == 'midday':
                        choices_functions, weights = self.midday_actions(selected_machine)
                    
                    elif self.period == 'afternoon':
                        choices_functions, weights = self.afternoon_actions(selected_machine)
                    
                    elif self.period == 'evening':
                        choices_functions, weights = self.evening_actions(selected_machine)
                    
                    elif self.period == 'night':
                        choices_functions, weights = self.night_actions(selected_machine)

                    if weights and len(choices_functions)>0:
                        # This will be in dataset as the agent that trigged the machine or turned it off
                        selected_machine.app.last_actor = self.human.name
                        selected_function = random.choices(choices_functions, weights=weights, k=1)[0]
                        if selected_function:
                            selected_function = getattr(selected_machine.app, selected_function, None)
                            if callable(selected_function):
                                # executing selected function
                                selected_function()

    def interact_to_current_environment_machines(self):
        """Chooses randonmicly a environment machine to interact to."""
        if self.human.current_environment:
            # if self.simulation_core.global_seed:
            #     random.seed(self.simulation_core.global_seed)
            
            if len(self.human.current_environment.machine_list) > 0:
                
                random.shuffle(self.human.current_environment.machine_list)
                # Select a machine randomly from environment machines list
                selected_machine = random.choice(self.human.current_environment.machine_list)
                
                # turn on or off the selected machine founded inside environment
                selected_machine.toggle_power_state()
                
                # This will be in dataset as the agent that trigged the machine or turned it off
                selected_machine.app.last_actor = self.human.name

    def run(self):
        LoopingCall(self.main_looping).start(self.human.simulation_core.clock.get_internal_time_unit(1))

    def main_looping(self):
        pass

class EnvironmentDrivenBehavior(BasicBehavior):

    def __init__(self, human):
        super().__init__(human)

    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()
        self.interact_to_current_environment_machines()


# time_table = {
#     # convert time to seconds at https://onlinetimetools.com/convert-time-to-seconds
#     "00:00 am": 0,
#     "06:59 am": 25140,
#     "07:00 am": 25200,
#     "11:59 am": 43140,
#     "22:00 pm": 79200,
#     "23:59 pm": 86399,
# }


class TimeDrivenBehavior(BasicBehavior):

    def __init__(self, human):
        super().__init__(human)
        self.human = human
        self.human.mobility = ProbabilisticGraphRandomWaypointMobility(
            self.human.visual_component,
            self.human.simulation_core,
            0.02,
            0.08,
            2,
            10,
            self.human
        )
        self.has_scheduled_scenes = False
        self.human.mobility.is_stopped = False

    def create_scenes(self):
        pass
    
    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()

        if not self.has_scheduled_scenes:
            self.create_scenes()
    
        if self.is_mid_night_or_dawn():
            if not self.human.is_at_bed() and not self.human.state == 'SLEEPING':
                # night period in seconds is 7x3600s = 25200s
                self.go_to_point_and_stay_at('BED', 'SLEEPING', 'AWAKE', 25200)

        elif self.is_morning():
            print('Its morning.....................................')
            
        elif self.is_midday():
            print('Its midday.....................................')

        elif self.is_afternoon():
            print('Its afternoon..................................')
        
        elif self.is_evening():
            print('Its evening..................................')
        
        elif self.is_night():
            print('Its night..................................')
        
        # interacts to environment appliances and nodes
        self.interact_to_current_environment_machines_weighted_choices()

    def is_mid_night_or_dawn(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(00,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(6,59)
            ):
                self.period = 'mid_night_or_dawn'
                return True
        return False
    
    def is_morning(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(7,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(11,59)
            ):
                self.period = 'morning'
                return True
        return False
    
    def is_midday(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(12,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(12,59)
            ):
                self.period = 'midday'
                return True
        return False
    
    def is_afternoon(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(13,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(16,59)
            ):
                self.period = 'afternoon'
                return True
        return False

    def is_evening(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(17,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(20,59)
            ):
                self.period = 'evening'
                return True
        return False
    
    def is_night(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(21,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(23,59)
            ):
                self.period = 'night'
                return True
        return False

    def morning_actions(self, machine):
        pass

    def midday_actions(self, machine):
        pass

    def afternoon_actions(self, machine):
        pass
    
    def evening_actions(self, machine):
        pass

    def night_actions(self, machine):
        pass
    
class MaleBehavior(TimeDrivenBehavior):

    def __init__(self, human):
        super().__init__(human)

    def create_scenes(self):
        super().create_scenes()
        self.has_scheduled_scenes = True
        scene = Scene(
            self.human.simulation_core,
            'Morning tasks',
            'Schedules tasks to be execute in the morning period'
        )
        scene.add_automation_scene('bed_room', 'Air Conditioner', 'turn_off', 43200)
        scene.add_automation_scene('living_room', 'SmartTv', 'turn_on', 120)
        scene.add_automation_scene('living_room', 'Ventilator', 'turn_on', 3600)
        self.human.simulation_core.smart_hub.app.all_scenes.append(scene)
        self.human.simulation_core.smart_hub.app.schedule_scenes()
        

    def morning_actions(self, machine):
        super().morning_actions(machine)
        choices_functions = []
        weights = ()
        if isinstance(machine.app, SmartTvApp):
            choices_functions = smarttv_functions
            weights = (50, 5, 15, 10, 10)

        elif isinstance(machine.app, VacuumBotApp):
            choices_functions = vaccumbot_functions
            weights = (80, 20)

        elif isinstance(machine.app, ShowerApp):
            choices_functions = shower_functions
            weights = (10, 85, 5)
        
        elif isinstance(machine.app, RefrigeratorApp):
            choices_functions = refrigerator_functions
            weights = (70, 2, 28)
        
        elif isinstance(machine.app, AirConditionerApp):
            choices_functions = air_conditioner_functions
            weights = (10, 75, 10, 5)
        
        elif isinstance(machine.app, VentilatorApp):
            choices_functions = ventilator_functions
            weights = (70, 10, 20)
            
        return choices_functions, weights
    
    def midday_actions(self, machine):
        super().midday_actions(machine)
        choices_functions = []
        weights = ()
        if isinstance(machine.app, SmartTvApp):
            choices_functions = smarttv_functions
            weights = (50, 5, 35, 5, 5)

        elif isinstance(machine.app, VacuumBotApp):
            choices_functions = vaccumbot_functions
            weights = (5, 95)

        elif isinstance(machine.app, ShowerApp):
            choices_functions = shower_functions
            weights = (5, 85, 0)
        
        elif isinstance(machine.app, RefrigeratorApp):
            choices_functions = refrigerator_functions
            weights = (70, 2, 28)
        
        elif isinstance(machine.app, AirConditionerApp):
            choices_functions = air_conditioner_functions
            weights = (5, 95, 0, 0)

        elif isinstance(machine.app, VentilatorApp):
            choices_functions = ventilator_functions
            weights = (88, 2, 10)

        return choices_functions, weights
    
    def afternoon_actions(self, machine):
        super().afternoon_actions(machine)
        choices_functions = []
        weights = ()
        if isinstance(machine.app, SmartTvApp):
            choices_functions = smarttv_functions
            weights = (50, 5, 35, 5, 5)

        elif isinstance(machine.app, VacuumBotApp):
            choices_functions = vaccumbot_functions
            weights = (95, 5)

        elif isinstance(machine.app, ShowerApp):
            choices_functions = shower_functions
            weights = (85, 15, 0)
        
        elif isinstance(machine.app, RefrigeratorApp):
            choices_functions = refrigerator_functions
            weights = (70, 2, 28)
        
        elif isinstance(machine.app, AirConditionerApp):
            choices_functions = air_conditioner_functions
            weights = (5, 95, 0, 0)

        elif isinstance(machine.app, VentilatorApp):
            choices_functions = ventilator_functions
            weights = (88, 2, 10)

        return choices_functions, weights
    
    def evening_actions(self, machine):
        super().evening_actions(machine)
        choices_functions = []
        weights = ()
        if isinstance(machine.app, SmartTvApp):
            choices_functions = smarttv_functions
            weights = (50, 5, 35, 5, 5)

        elif isinstance(machine.app, VacuumBotApp):
            choices_functions = vaccumbot_functions
            weights = (0, 0)

        elif isinstance(machine.app, ShowerApp):
            choices_functions = shower_functions
            weights = (75, 15, 10)
        
        elif isinstance(machine.app, RefrigeratorApp):
            choices_functions = refrigerator_functions
            weights = (70, 2, 28)
        
        elif isinstance(machine.app, AirConditionerApp):
            choices_functions = air_conditioner_functions
            weights = (45, 55, 0, 0)
        
        elif isinstance(machine.app, VentilatorApp):
            choices_functions = ventilator_functions
            weights = (10, 70, 20)

        return choices_functions, weights
    
    def night_actions(self, machine):
        super().night_actions(machine)
        choices_functions = []
        weights = ()
        if isinstance(machine.app, SmartTvApp):
            choices_functions = smarttv_functions
            weights = (50, 5, 35, 5, 5)

        elif isinstance(machine.app, VacuumBotApp):
            choices_functions = vaccumbot_functions
            weights = (0, 0)

        elif isinstance(machine.app, RefrigeratorApp):
            choices_functions = refrigerator_functions
            weights = (70, 2, 28)
        
        elif isinstance(machine.app, AirConditionerApp):
            choices_functions = air_conditioner_functions
            weights = (85, 5, 10, 0)
        
        elif isinstance(machine.app, VentilatorApp):
            choices_functions = ventilator_functions
            weights = (10, 70, 20)

        return choices_functions, weights