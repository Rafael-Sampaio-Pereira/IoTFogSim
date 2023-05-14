
from apps.base_app import BaseApp
from mobility.random_walk_mobility import RandomWalkMobility

class VacuumBotApp(BaseApp):

    def __init__(self):
        super(VacuumBotApp, self).__init__()
        self.name = 'Vaccum Bot'
        self.is_moving = False

    def main(self):
        super().main()
        if self.machine.is_turned_on:
            self.run_mobility()

    def run_mobility(self):
        if not self.is_moving:
            RandomWalkMobility(
                self.machine.visual_component,
                self.simulation_core,
                30
            )
            self.is_moving = True
        