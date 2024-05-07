from twisted.internet.task import LoopingCall
import random
from twisted.internet import reactor
from apps.air_conditioner import AirConditionerApp
from apps.light_bulb import LightBulbApp
from apps.microwave import MicrowaveApp
from apps.refrigerator import RefrigeratorApp
from apps.shower import ShowerApp
from apps.smart_hub import Scene
from apps.smart_tv import SmartTvApp
from apps.vacuum_bot import VacuumBotApp
from apps.ventilator import VentilatorApp
from core.functions import readable_time_to_seconds
import os
import json
from core.functions import sleep
from twisted.internet.defer import inlineCallbacks
from core.functions import get_all_methods_and_attributes_from_instance

from mobility.task_based_graph_random_waypoint_mobility import TaskBasedGraphRandomWaypointMobility
        
class Task(object):
    def __init__(
        self,
        point,
        actor_name,
        code,
        title,
        duration,
        device_name,
        function_to_call,
        parameters,
        dependencies=None
    ):
        self.point = point
        self.actor_name = actor_name
        self.code = code
        self.title = title
        self.duration = duration
        self.device_name = device_name
        self.function_to_call = function_to_call
        self.parameters = parameters
        self.dependencies = dependencies or []
        self.completed = False
        self.human = None
    
    @inlineCallbacks 
    def run(self):
        print(f"Executando a tarefa: {self.title}")
        
        #  - configura o proximo ponto e vai para lá
        #  - verifica se já chegou no ponto, se sim:
        #      - executa a função principal da tarefa
        #      - espera o tempo de ruração da tarefa
        
        self.human.mobility.set_next_mobility_point("POINT_2")
        yield sleep(self.duration)
        print(f"Tarefa concluída: {self.title}")


class TaskScheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.code] = task

    def run_task(self, task_code):
        print("VEIO ATÉ AQUI", task_code)
        task = self.tasks.get(task_code)
        print("VEIO ATÉ AQUI TBM ....", task.code)
        if task:
            # if not task.completed:
            # if not task.completed:
            if len(task.dependencies) > 0:
                print("VEIO ATÉ AQUI VELHAOOOOOO", len(task.dependencies))
                for dependency in task.dependencies:
                    self.run_task(dependency)
                    # task.completed = True
            task.run()


class TaskDrivenBehavior(object):
    def __init__(self, human):
        self.human = human
        self.min_pause_time = 2
        self.max_pause_time = 10
        self.scheduler = TaskScheduler()
        self.human.mobility = TaskBasedGraphRandomWaypointMobility(
            self.human.visual_component,
            self.human.simulation_core,
            0.02,
            0.08,
            self.min_pause_time,
            self.max_pause_time,
            self.human
        )
        self.load_tasks()
        self.scheduler.run_task("ATV01")
    
    # def go_to_point_and_stay_at(self, point_name, state_before, state_after, duration):
    #     self.human.mobility.set_next_mobility_point(point_name)
    #     reactor.callLater(
    #         self.human.simulation_core.clock.get_internal_time_unit(20),
    #         self.human.set_state,
    #         state_before
    #     )
    #     reactor.callLater(
    #         self.human.simulation_core.clock.get_internal_time_unit(duration),
    #         self.human.set_state,
    #         state_after
    #     )


    def run(self):
        LoopingCall(self.main_looping).start(self.human.simulation_core.clock.get_internal_time_unit(1))

    def main_looping(self):
        pass
    
    def load_tasks(self):
        # create tasks
        print(self.human.simulation_core.project_name, "EM TESTE")
        file_path = 'projects/'+self.human.simulation_core.project_name+'/task.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as tasks_file:
                data = json.loads(tasks_file.read())
                if data:
                    for task in data:
                        _task = Task(
                            task["point"],
                            task["actor_name"],
                            task["code"],
                            task["title"],
                            task["duration"],
                            task["device_name"],
                            task['function_to_call'],
                            task["parameters"],
                            task["dependencies"]
                        )
                        _task.human = self.human
                        # Adding tasks to the scheduler
                        self.scheduler.add_task(_task)

