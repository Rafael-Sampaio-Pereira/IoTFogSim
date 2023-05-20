from apps.base_app import BaseApp

class Light(object):
    def __init__(self):
        pass

class LightBulbApp(BaseApp, Light):
    def __init__(self):
        super(LightBulbApp, self).__init__()
        self.name = 'LightBulbApp'
        
    def set_simulation_core(self, simulation_core):
        simulation_core.canvas.itemconfig(
            self.machine.visual_component.draggable_img, tags=("light_bulb",)
        )   
