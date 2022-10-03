import uuid


class NetworkInterface(object):
    def __init__(self, simulation_core, name, is_wireless, ip, machine):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().hex
        self.name = name
        self.is_wireless = is_wireless
        self.ip = ip
        self.machine = machine