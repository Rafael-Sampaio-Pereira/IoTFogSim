import time

class Task:
    def __init__(self, name, dependencies=None):
        self.name = name
        self.dependencies = dependencies or []
        self.completed = False

    def run(self):
        print(f"Executando a tarefa: {self.name}")
        # Simula a execução da tarefa
        time.sleep(1)
        print(f"Tarefa concluída: {self.name}")

class TaskScheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.name] = task

    def run_task(self, task_name):
        task = self.tasks.get(task_name)
        if task:
            # if not task.completed:
            if not task.completed:
                for dependency in task.dependencies:
                    self.run_task(dependency)
                    task.completed = True
                task.run()

# Criando as tarefas
task1 = Task("Tarefa 1")
task2 = Task("Tarefa 2", dependencies=["Tarefa 1"])
task3 = Task("Tarefa 3", dependencies=["Tarefa 1", "Tarefa 2"])
task4 = Task("Tarefa 4", dependencies=["Tarefa 2",])
task5 = Task("Tarefa 5", dependencies=["Tarefa 3", "Tarefa 4"])
task6 = Task("Tarefa 6", dependencies=["Tarefa 4"])
task7 = Task("Tarefa 7", dependencies=["Tarefa 5", "Tarefa 6"])

# Criando o agendador
scheduler = TaskScheduler()

# Adicionando as tarefas ao agendador
scheduler.add_task(task1)
scheduler.add_task(task2)
scheduler.add_task(task3)
scheduler.add_task(task4)
scheduler.add_task(task5)
scheduler.add_task(task6)
scheduler.add_task(task7)

# Executando as tarefas
scheduler.run_task("Tarefa 6")