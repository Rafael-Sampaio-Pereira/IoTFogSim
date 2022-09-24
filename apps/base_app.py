import uuid


class BaseApp(object):
    def __init__(self):
        self.simulation_core = None
        self.id = uuid.uuid4().hex
        self.name = 'my_app'
        self.port = 80
        self.protocol = 'TCP' # can be UDP or TCP
        self.machine = None
        self.in_buffer = set()

    def main(self):
        pass

    def start(self):
        self.simulation_core.updateEventsCounter(f"Info : - | {self.name} - Initializing app.")

    def send_packet(self):
        pass

class ServerApp(BaseApp):
    def __init__(self):
        super(ServerApp, self).__init__()   

class RouterApp(BaseApp):
    def __init__(self):
        super(RouterApp, self).__init__()

class RouterWithAccessPointApp(RouterApp):
    def __init__(self):
        super(RouterWithAccessPointApp, self).__init__() 