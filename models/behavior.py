from twisted.internet.task import LoopingCall
import random
from twisted.internet import reactor

from mobility.probabilistic_graph_random_waypoint_mobility import ProbabilisticGraphRandomWaypointMobility


class BasicBehavior(object):
    def __init__(self, human):
        self.human = human

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


time_table = {
    # convert time to seconds at https://onlinetimetools.com/convert-time-to-seconds
    "00:00 am": 0,
    "06:59 am": 25140,
    "07:00 am": 25200,
    "11:59 am": 43140,
    "22:00 pm": 79200,
    "23:59 pm": 86399,
}


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
                clock.elapsed_seconds >= time_table["22:00 pm"]
                    and
                clock.elapsed_seconds <= time_table["23:59 pm"]
            ):
                return True
        if (
                clock.elapsed_seconds >= time_table["00:00 am"]
                    and
                clock.elapsed_seconds <= time_table["06:59 am"]
            ):
                return True
        return False
    
    def is_morning(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= time_table["07:00 am"]
                    and
                clock.elapsed_seconds <= time_table["11:59 am"]
            ):
                return True
        return False
    
    def is_midday(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= time_table["12:00 am"]
                    and
                clock.elapsed_seconds <= time_table["12:59 pm"]
            ):
                return True
        return False
    
    def is_afternoon(self) -> bool:
        clock = self.human.simulation_core.clock
        if (
                clock.elapsed_seconds >= time_table["13:00 pm"]
                    and
                clock.elapsed_seconds <= time_table["16:59 pm"]
            ):
                return True
        return False

    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()
    
        if self.is_mid_night_or_dawn():
            if not self.human.is_at_bed() and not self.human.state == 'SLEEPING':
                self.go_to_point_and_stay_at('BED', 'SLEEPING', 'AWAKE', 3600)

        elif self.is_morning():
            print('Its morning....................................')

        elif self.is_midday():
            print('Its midday.....................................')

        elif self.is_afternoon():
            print('Its afternoon..................................')
            
