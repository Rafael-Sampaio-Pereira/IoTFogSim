import os
import json
from core.functions import sleep
from twisted.internet.defer import inlineCallbacks
from core.functions import get_all_methods_and_attributes_from_instance
from twisted.internet import reactor

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
        dependencies
    ):
        self.point = point
        self.actor_name = actor_name
        self.code = code
        self.title = title
        self.duration = duration
        self.device_name = device_name
        self.function_to_call = function_to_call
        self.parameters = parameters
        self.dependencies = dependencies
        self.is_function_at_queue = False

class Device(object):
    def __init__(self, name, power):
        self.name = name
        self.power = power
        
    def get_name(self):
        return self.name

    def get_power(self):
        return self.power

device_list = [
    {
        "name": "Air",
        "power": 2000
    },
    {
        "name": "Computer",
        "power": 100
    },
    {
        "name": "Refrigerator",
        "power": 500
    },
    {
        "name": "Bed",
        "power": 350
    }
]

all_devices = []

for device in device_list:
    _device = Device(device["name"], device["power"])
    all_devices.append(_device)
    
all_tasks_list = []

def load_tasks():
    file_path = 'task.json'
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
                    all_tasks_list.append(_task)                                        
                    
load_tasks()

task_functions_queue = []

def get_task_device_function_to_call(task):

    device = next(filter(
        lambda _device: _device.name == task.device_name,
        all_devices), None)
    
    if device:
        valid_commands = get_all_methods_and_attributes_from_instance(device)
        if task.function_to_call in valid_commands:
            fn = getattr(device, task.function_to_call, None)
            if callable(fn):
                # device.app.last_actor = self.scene.simulation_core.smart_hub.name
                return fn

def schedule_tasks_functions(first_task):

        if len(first_task.dependencies) > 0:
            for dependency in first_task.dependencies:
                _dependency = next(
                    filter(lambda tsk: tsk.code == dependency, all_tasks_list),
                    None
                )
                if _dependency and not _dependency.is_function_at_queue:
                    _dependency.is_function_at_queue = True
                    schedule_tasks_functions(_dependency)
        
        fn = get_task_device_function_to_call(first_task)
        if fn:
            first_task.is_function_at_queue = True
            task_functions_queue.append((fn, first_task.duration))
            

for task in all_tasks_list:
    schedule_tasks_functions(task)


print(task_functions_queue)

@inlineCallbacks 
def  process_tasks():

    for task_function in task_functions_queue:
        print(task_function[0]())
        yield sleep(task_function[1])

process_tasks()

if __name__ == '__main__':
    reactor.run()