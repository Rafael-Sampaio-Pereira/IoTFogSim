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


def extract_package_contents(msg):
    
    try:
        msg = msg.decode("utf-8")
        msg = str(msg)[0:]
        json_msg = json.loads(msg)

        return json_msg["destiny_addr"], json_msg["destiny_port"], json_msg["source_addr"], json_msg["source_port"], json_msg["type"], json_msg["payload"]
    
    except Exception as e:
        log.msg(e)