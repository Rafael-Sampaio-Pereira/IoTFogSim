from twisted.internet.task import LoopingCall
import random
from twisted.internet import reactor
from apps.air_conditioner import AirConditionerApp
from apps.refrigerator import RefrigeratorApp
from apps.shower import ShowerApp
from apps.smart_hub import Scene
from apps.smart_tv import SmartTvApp
from apps.vacuum_bot import VacuumBotApp
from core.functions import readable_time_to_seconds

from mobility.probabilistic_graph_random_waypoint_mobility import ProbabilisticGraphRandomWaypointMobility


class BasicBehavior(object):
    def __init__(self, human):
        self.human = human
        self.period = None

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


class TimeDriverBehavior(BasicBehavior):

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

    def is_mid_night_or_dawn(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(22,00) 
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(23,59)
            ):
                self.period = 'night_or_dawn'
                return True
        if (
                clock.elapsed_seconds >= readable_time_to_seconds(00,00)
                    and
                clock.elapsed_seconds <= readable_time_to_seconds(6,59)
            ):
                self.period = 'night_or_dawn'
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

    def create_scenes(self):
        self.has_scheduled_scenes = True
        scene = Scene(
            self.human.simulation_core,
            'Morning tasks',
            'Schedules tasks to be execute in the morning period'
        )
        scene.add_automation_scene('bed_room', 'Air Conditioner', 'turn_off', 60)
        self.human.simulation_core.smart_hub.app.all_scenes.append(scene)
        self.human.simulation_core.smart_hub.app.schedule_scenes()
        
    
    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()

        if not self.has_scheduled_scenes:
            self.create_scenes()
    
        if self.is_mid_night_or_dawn():
            if not self.human.is_at_bed() and not self.human.state == 'SLEEPING':
                self.go_to_point_and_stay_at('BED', 'SLEEPING', 'AWAKE', 3600)

        elif self.is_morning():
            print('Its morning.....................................')
            
        elif self.is_midday():
            print('Its midday.....................................')

        elif self.is_afternoon():
            print('Its afternoon..................................')
        
        # interacts to environment appliances and nodes
        self.interact_to_current_environment_machines_weighted_choices()

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
                        if isinstance(selected_machine.app, SmartTvApp):
                            choices_functions = [
                                'turn_on',
                                'turn_off',
                                'set_channel',
                                'set_volume',
                                'set_source'
                            ]
                            weights = (50, 5, 15, 10, 10)

                        elif isinstance(selected_machine.app, VacuumBotApp):
                            choices_functions = [
                                'turn_on',
                                'turn_off',
                            ]
                            weights = (80, 20)


                        elif isinstance(selected_machine.app, ShowerApp):
                            choices_functions = [
                                'turn_on',
                                'turn_off',
                                'set_temperature'
                            ]
                            weights = (10, 85, 5)
                        
                        elif isinstance(selected_machine.app, RefrigeratorApp):
                            choices_functions = [
                                'turn_on',
                                'turn_off',
                                'set_temperature'
                            ]
                            weights = (70, 2, 28)
                        
                        elif isinstance(selected_machine.app, AirConditionerApp):
                            choices_functions = [
                                'turn_on',
                                'turn_off',
                                'set_temperature',
                                'set_fan_speed'
                            ]
                            weights = (10, 75, 10, 5)
                    
                    if weights and len(choices_functions)>0:
                        # This will be in dataset as the agent that trigged the machine or turned it off
                        selected_machine.app.last_actor = self.human.name
                        selected_function = random.choices(choices_functions, weights=weights, k=1)[0]
                        if selected_function:
                            selected_function = getattr(selected_machine.app, selected_function, None)
                            if callable(selected_function):
                                # executing selected function
                                selected_function()
                
            
