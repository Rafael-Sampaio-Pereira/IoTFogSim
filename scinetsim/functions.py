from twisted.python import log
from importlib import import_module
import json

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