from twisted.python import log
from importlib import import_module
import json

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


