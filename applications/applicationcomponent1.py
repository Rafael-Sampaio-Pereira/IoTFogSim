from twisted.python import log
import tkinter
from config.settings import ICONS_PATH

class StandardClientApplicationComponent():
    
    def __init__(self, visual_component, canvas):
        self.visual_component = visual_component
        self.canvas = canvas

    def onConnectionReceived(self):
        pass
    
    def sendPackt(self, destiny_host, message):
        pass

    def onPacktReceive(self):
        pass

    def buildPackt(self):
        pass




class StandardServerApplicationComponent():
    
    def __init__(self, visual_component, canvas):
        self.visual_component = visual_component
        self.canvas = canvas

    def onConnectionReceived(self):
        pass
    
    def sendPackt(self, destiny_host, message):
        pass

    def onPacktReceive(self):
        pass    

    def buildPackt(self):
        pass
