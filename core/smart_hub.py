
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


                    
class SmartHubApp():

    def __init__(self, simulation_core):
        self.simulation_core = simulation_core
        self.name ='Smart Hub Controller'
        self.activity_table = [
            {"addr": "192.168.1.3", "starts_at": "0:09:00", "ends_at": "0:20:00"},
            # {"addr": "", "port": "", "starts_at": "0:12:00", "ends_at": "0:30:00"},
        ]
        
    def start(self):
        LoopingCall(self.main_loop).start(self.simulation_core.clock.get_internal_time_unit(60))
        
    def main_loop(self):
        now = self.simulation_core.clock.get_humanized_time()
        
        for machine_activity in self.activity_table:
            if machine_activity['starts_at'] == now:
                machine = self.simulation_core.get_machine_by_ip(machine_activity['addr'])
                machine.turn_on()
            elif machine_activity['ends_at'] == now:
                machine = self.simulation_core.get_machine_by_ip(machine_activity['addr'])
                machine.turn_off()


colocar instancia no simulation core e criar arquivo json  de tabela de atividades