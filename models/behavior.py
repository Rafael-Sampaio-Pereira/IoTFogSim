from twisted.internet.task import LoopingCall
import random


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
        LoopingCall(self.main_looping).start(1)

    def main_looping(self):
        pass

class EnvironmentDrivenBehavior(BasicBehavior):

    def __ini__(self, human):
        super().__init__(human)

    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()
        self.interact_to_current_environment_machines()


time_table = {
    # convert time to seconds at https://onlinetimetools.com/convert-time-to-seconds
    "00:00 am": 0,
    "07:00 am": 25200,
    "22:00 pm": 79200,
    "23:59 pm": 86399,
}


class TimeDriverBehavior(BasicBehavior):

    def __ini__(self, human):
        super().__init__(human)
        self.human = human

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
                clock.elapsed_seconds <= time_table["07:00 am"]
            ):
                return True
        return False

    def main_looping(self):
        super().main_looping()
        self.human.check_current_environment()
    
        if self.is_mid_night_or_dawn():
            print("IT'S TIME TO SLEEP")

        
            