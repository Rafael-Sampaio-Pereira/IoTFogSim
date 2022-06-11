import json
from twisted.python import log
from importlib import import_module
import inspect
import importlib
import os
from fabric.api import local
import netifaces


def import_and_instantiate_class_from_string(class_path):

    # the classPath needs to be = folder.file.class - Rafael Sampaio

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


# This configure function let us to observ logs in screen while they are save in a log file - Rafael Sampaio
def configure_logger(log_file_path, project_name):
    from sys import stdout
    from twisted.logger import Logger, textFileLogObserver, globalLogBeginner
    from datetime import datetime, date
    import os

    # create logs directoy if it not exist - Rafael Sampaio
    os.makedirs(log_file_path+"/logs/", exist_ok=True)
    temp = "_{:%Y_%m_%d__%H_%M_%S}".format(datetime.now())
    log_file = log_file_path+"/logs/"+project_name+temp+".log"
    logfile = open(log_file, 'a')
    globalLogBeginner.beginLoggingTo([
        textFileLogObserver(stdout),
        textFileLogObserver(logfile)])
    log = Logger()


def create_csv_database_file(simulation_core, description=""):
    from datetime import datetime, date
    import os

    file_path = "projects/"+simulation_core.project_name+"/"

    # create databases directoy if it not exist - Rafael Sampaio
    os.makedirs(file_path+"/databases/", exist_ok=True)
    temp = "_{:%Y_%m_%d__%H_%M_%S}".format(datetime.now())
    file = file_path+"/databases/" + \
        simulation_core.project_name+temp+"_"+description+".csv"
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


# getting the default interface name - Rafael Sampaio
def get_default_interface():
    return netifaces.gateways()['default'][netifaces.AF_INET][1]

# clear all changes made in a given network interface - Rafael Sampaio


def clear_network_changes(interface):
    local(f"sudo tc qdisc del dev {interface} root")


def extract_mqtt_contents(package):
    try:
        package = json.dumps(package)
        package = str(package)[0:]
        json_msg = json.loads(package)
        return json_msg["action"], json_msg["topic"], json_msg["content"]
    except Exception as e:
        log.msg(e)
