import json
import random
from twisted.python import log
from importlib import import_module
import inspect
import importlib
import os
from fabric.api import local
import netifaces
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from twisted.internet.task import deferLater
from datetime import datetime, date
import os


def sleep(secs):
    """Provide a non-blocking sleep function.
        any method that will use that function inside needs to use the @inlineCallbacks decorator.
        Example: it can be use to control a for iteration time.
        secs: float - Number of seconds to be waiting.
    """
    return deferLater(reactor, secs, lambda: None)


def import_and_instantiate_class_from_string(class_path):

    # the classPath needs to be = folder.file.class

    try:
        paths = class_path.split('.')
        module_path = paths[0]+"."+paths[1]
        class_name = paths[2]
        module = import_module(module_path)
        _class = getattr(module, class_name)
        class_instance = _class()
        return class_instance

    except Exception as e:
        log.msg(e)


# This configure function let us to observ logs in screen while they are save in a log file
def configure_logger(log_file_path, project_name):
    from sys import stdout
    from twisted.logger import Logger, textFileLogObserver, globalLogBeginner
    import os

    # create logs directoy if it not exist
    os.makedirs(log_file_path, exist_ok=True)
    log_file = log_file_path+project_name+"_events.log"
    logfile = open(log_file, 'a')
    globalLogBeginner.beginLoggingTo([
        textFileLogObserver(stdout),
        textFileLogObserver(logfile)])
    log = Logger()


def create_csv_database_file(simulation_core, description=""):
    from datetime import datetime
    import os

    file_path = "projects/"+simulation_core.project_name+"/"

    # create databases directoy if it not exist
    os.makedirs(file_path+"/databases/", exist_ok=True)
    temp = "_{:%Y_%m_%d__%H_%M_%S}".format(datetime.now())
    file = file_path+"/databases/" + \
        simulation_core.project_name+temp+"_"+description+".csv"
    database = open(file, 'a')

    return database


def create_csv_results_file(simulation_core, description=""):
    # create results directoy if it not exist
    os.makedirs(simulation_core.output_dir+"/results/", exist_ok=True)
    file = simulation_core.output_dir+"/results/"+simulation_core.project_name+"_"+description+".csv"
    database = open(file, 'a')

    return database


def get_all_app_classes_name():
    directory = 'applications'

    app_files = [f.name for f in os.scandir(directory) if f.is_file()]
    app_list = []
    for file in app_files:
        module = importlib.import_module('applications.'+file[:-3])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if(name.endswith('App')):
                app_list.append(file[:-3]+'.'+name)

    return app_list


def extract_mqtt_contents(package):
    try:
        package = json.dumps(package)
        package = str(package)[0:]
        json_msg = json.loads(package)
        return json_msg["action"], json_msg["topic"], json_msg["content"]
    except Exception as e:
        log.msg(e)


def get_random_color(global_seed=None):
    if global_seed:
        random.seed(global_seed)
    colors = [
            '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
            '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
            '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
            '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
            '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
            '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
            '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
            '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
            '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
            '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'
    ]
    return random.choice(colors)

def cline(x1, y1, x2, y2):
    # Autor: John Clark Craig
    # Available at https://jccraig.medium.com/we-must-draw-the-line-1820d49d19dd
    all_coords = []
    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1 if x1 > x2 else 0
    sy = 1 if y1 < y2 else -1 if y1 > y2 else 0
    ix = dy // 2
    iy = dx // 2
    pixels = dx + 1 if dx > dy else dy + 1
    while pixels:
        all_coords.append((x, y))
        ix += dx
        if ix >= dy:
            ix -= dy
            x += sx
        iy += dy
        if iy >= dx:
            iy -= dx
            y += sy
        pixels -= 1
        
    all_coords.append((x2, y2))
    return all_coords
    
def get_all_methods_and_attributes_from_instance(instance):
    return [ cmd for cmd in dir(instance) if not cmd.startswith('__')]

def close_terminal():
    import os
    import signal
    os.kill(os.getppid(), signal.SIGHUP)