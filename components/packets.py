import datetime
import uuid
        

class Packet(object):
    def __init__(
            self,
            simulation_core,
            source_addr,
            source_port,
            destiny_addr,
            destiny_port,
            payload,
            length,
            color=None
        ):
        self.simulation_core = simulation_core
        self.id = uuid.uuid4().fields[-1]
        self.source_addr = source_addr
        self.source_port = source_port
        self.destiny_addr = destiny_addr
        self.destiny_port = destiny_port
        self.payload = payload
        self.trace = []
        self.length = length
        self.created_at = datetime.datetime.now().isoformat()
        self.last_link = None
        self.color = color