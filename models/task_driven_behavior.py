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
from twisted.internet.task import cooperate
import os
import json
import time
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
        dependencies=None
    ):
        self.point = point
        self.actor_name = actor_name
        self.code = code
        self.title = title
        self.duration = duration
        self.device_name = device_name
        self.function_to_call = function_to_call
        self.dependencies = dependencies or []
        self.completed = False
        self.human = None
        self.task_queue = []
        
        
    
    def run(self):
        @inlineCallbacks 
        def core():
            for task in self.task_queue:
                print(f"Executando a tarefa: {task.title}")
                # nao funciona vai para um ponto porem nao chega aos demais
                self.human.mobility.set_next_mobility_point(task.point)
                self.human.mobility.move()
                #  waiting for human to get destiny point

                # call task main function
                if task.function_to_call:
                    task.function_to_call()
                
                # waitng time for call next task
                yield sleep(task.duration)
            
                print(f"Tarefa concluída: {task.title}")
        
        cooperate(core())
            
    
class TaskScheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.code] = task


class TaskDrivenBehavior(object):
    def __init__(self, human):
        self.human = human
        self.scheduler = TaskScheduler()
        self.all_task_list = []
        self.human.mobility = TaskBasedGraphRandomWaypointMobility(
            self.human.visual_component,
            self.human.simulation_core,
            0.02,
            0.08,
            self.human
        )
        self.load_tasks()
        for _task in self.all_task_list:
            self.schedule_tasks_functions(_task, _task.task_queue)
            self.scheduler.add_task(_task)
        
    def run(self):
        self.all_task_list[2].run()
        # self.scheduler.run_task("ATV03")
        # LoopingCall(self.main_looping).start(self.human.simulation_core.clock.get_internal_time_unit(1))

    def main_looping(self):
        """ COLOCAR AQUI A IMPLEMENTAÇÃO DO SCHEDULER QUE VERIFICARÁ O VALOR DA TEMPERATURA E DA LUMINOSIDADE"""
        pass
    
    def load_tasks(self):
        # create tasks
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
                            task["dependencies"]
                        )
                        _task.human = self.human
                        _task.function_to_call = self.get_task_device_function_to_call(task)
                        self.all_task_list.append(_task)
                        

    def schedule_tasks_functions(self, _task, queue):

            if len(_task.dependencies) > 0:
                for dependency in _task.dependencies:
                    _dependency = next(
                        filter(lambda tsk: tsk.code == dependency, self.all_task_list),
                        None
                    )
                    self.schedule_tasks_functions(_dependency, queue)
            
            if _task:
                queue.append(_task)
                
    
    def get_task_device_function_to_call(self, task):

        device = next(filter(
            lambda _device: _device.name == task["device_name"],
            self.human.simulation_core.all_machines), None)
        
        if device:
            valid_commands = get_all_methods_and_attributes_from_instance(device)
            if task["function_to_call"] in valid_commands:
                fn = getattr(device, task["function_to_call"], None)
                if callable(fn):
                    # device.app.last_actor = self.scene.simulation_core.smart_hub.name
                    return fn


