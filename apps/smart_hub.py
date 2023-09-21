
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from core.functions import get_all_methods_and_attributes_from_instance, sleep

class Scene(object):
    def __init__(
            self,
            simulation_core,
            name,
            description
        ):
        self.simulation_core = simulation_core
        self.name = name
        self.description = description
        self.activity_table = []

    def add_automation_scene(
            self,
            environment,
            device,
            function_to_call,
            trigger_after
        ):
        """ duration expressed in seconds"""
        self.activity_table.append(
            SceneActivity(
                self,
                environment,
                device,
                function_to_call,
                trigger_after
            )
        )

class SceneActivity(object):
    def __init__(
            self,
            scene,
            environment,
            device,
            function_to_call,
            trigger_after
        ):
        self.scheduled = False
        self.fired = False
        self.failed = False
        self.scene = scene
        self.environment = environment
        self.device = device
        self.function_to_call = function_to_call
        self.trigger_after = trigger_after

    def fire(self):
        # 1st verify if environment exists
        # second verify if device exists into environment
        # 3rd verify if founded device has the function which is 
        # desired to be called, by looking into all valids commands
        environment = next(filter(
                lambda env: env.name == self.environment,
                self.scene.simulation_core.all_environments), None)
        if environment:
            device = next(filter(
                lambda dev: dev.name == self.device,
                environment.machine_list), None)
            if device:
                valid_commands = get_all_methods_and_attributes_from_instance(device)
                if self.function_to_call in valid_commands:
                    fn = getattr(device, self.function_to_call, None)
                    if callable(fn):
                        device.app.last_actor = self.scene.simulation_core.smart_hub.name
                        fn()
        else:
            self.failed = True

    def schedule(self):
        if not self.scheduled:
            self.scheduled = True
            if not self.fired :
                self.fired = True
                reactor.callLater(self.trigger_after, self.fire)
        

        

                    
class SmartHub(object):

    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.name ='Alexa'
        self.all_scenes = []
        self.running_scene = None
        
    def start(self):
        self.schedule_scenes()
        # LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(60))

    def schedule_scenes(self):
        if len(self.all_scenes)>0:
            for scene in self.all_scenes:
                if len(scene.activity_table)>0:
                    for activity in scene.activity_table:
                        activity.schedule()
        
    # def main_loop(self):
    #     now = self.simulation_core.clock.get_humanized_time()

        # for scene in self.all_scenes:
        
        # for machine_activity in self.activity_table:
        #     if machine_activity['starts_at'] == now:
        #         machine = self.simulation_core.get_machine_by_ip(machine_activity['addr'])
        #         machine.turn_on()
        #     elif machine_activity['ends_at'] == now:
        #         machine = self.simulation_core.get_machine_by_ip(machine_activity['addr'])
        #         machine.turn_off()




# COLOCAR SMART HUB COMO UM DEVICE E ICON DE ALEXA
# CRIAR AGENDAMENTO DE TAREFAS
# TESTAR AGENDAMENTO 