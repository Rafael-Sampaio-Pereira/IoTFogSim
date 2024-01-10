import psutil
import re
import os
from twisted.internet.task import LoopingCall
from core.functions import get_last_dir_inside_of
import datetime
import sys
from twisted.internet import reactor


def update_memory_and_cpu_usage_file(memory_and_cpu_usage_file, pid):
    """THis will get main process memory and cpu usage, as well as they children processes"""
    
    my_process = psutil.Process(pid)
    cpu_percent = my_process.cpu_percent(interval=1) / psutil.cpu_count()
    for child in my_process.children(recursive=True):
        cpu_percent += child.cpu_percent(1) / psutil.cpu_count()
        
    cpu_percent = round(cpu_percent,2)
    
    # RSS - resident set size, the non-swapped physical memory that a task
    # has used (in kiloBytes).  (alias rssize, rsz).
    memory = my_process.memory_info().rss
    for child in my_process.children(recursive=True):
        memory += child.memory_info().rss
    
    memory = round((memory/1048576),2)  # 1024*1024 = 1048576 - to ger value in Mb
    def get_row():
        row = \
        f"{str(datetime.datetime.now())};"+\
        f"{pid};"+\
        f"{cpu_percent};"+\
        f"{memory}"
        return row
    
    print(get_row(), file = memory_and_cpu_usage_file, flush=True)
    print(f"Analising cpu and memory - PID: {pid} | CPU: {cpu_percent}% | RAM: {memory}Mb")


if __name__ == '__main__':
    os.makedirs(get_last_dir_inside_of('outputs')+"/results/", exist_ok=True)
    memory_and_cpu_usage_file = open(get_last_dir_inside_of('outputs')+"/results/CPU_n_RAM.csv", 'a')
    header = 'time; pid; cpu(%); memory(Mb)'
    print(header, file = memory_and_cpu_usage_file, flush=True)
    pid = int(open(get_last_dir_inside_of('outputs')+"/process_id.info").read())
    LoopingCall(update_memory_and_cpu_usage_file, memory_and_cpu_usage_file,pid).start(1)
    reactor.run()
