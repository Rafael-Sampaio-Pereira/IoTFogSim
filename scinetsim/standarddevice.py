
from twisted.internet import protocol, reactor,endpoints
from twisted.python import log
from utils.draggableImage import DraggableImage
import tkinter
from config.settings import ICONS_PATH


class StandardApplicationComponent(protocol.Protocol):
    def __int__(self):
        pass

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
    
    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
    
    def send(self, message):
        self.transport.write(message)




class VisualComponent(object):

    def __init__(self, canvas, deviceName, file, x, y):
        self.canvas = canvas
        self.image_file = tkinter.PhotoImage(file=file)
        self.draggable_img = self.canvas.create_image(x, y, image=self.image_file)

        self.draggable_name = self.canvas.create_text(x,y+27,fill="black",font="Times 9",
                        text=deviceName)
        # font="Times 9 italic bold"
         
        canvas.tag_bind(self.draggable_name, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_name, '<ButtonRelease-1>', self.release)
        canvas.tag_bind(self.draggable_img, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_img, '<ButtonRelease-1>', self.release)
        canvas.configure(cursor="hand1")
        self.move_flag = False
         
    def move(self, event):
        if self.move_flag:
            new_xpos = event.x
            new_ypos = event.y
             
            self.canvas.move(self.draggable_name,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.canvas.move(self.draggable_img,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.draggable_img)
            self.canvas.tag_raise(self.draggable_name)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False


class StandardServerDevice():
    
    def __init__(self):
        self.canvas = None
        self.icon = None
        self.name = "Server"
        self.network_component = StandardServerNetworkComponent()

    def setCanvas(self, canvas):
        self.canvas = canvas

    def run(self):
        self.icon = VisualComponent(self.canvas, self.name, ICONS_PATH+"scinetsim_restfull_server.png", 100, 100)
        endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)



class StandardServerNetworkComponent():

    def __init__(self, host=None, port=None):
        self.host = host or "127.0.0.1"
        self.port = port or 5000
        self.network_settings = "tcp:interface={}:{}".format(str(self.host),self.port)
        print(self.network_settings)

    def doStart(self):
        log.msg("Initializing Server...")
    
    def doStop(self):
        log.msg("Shotdown Server...")
    
    def buildProtocol(self, addr):
        return StandardApplicationComponent()


class StandardClientNetworkComponent():

    def __init__(self, serverHost=None, serverPort=None):
        self.serverHost = serverHost or "127.0.0.1"
        self.serverPort = serverPort or  5000
        self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)

    def doStart(self):
        log.msg("Initializing client...")
    
    def doStop(self):
        log.msg("Shotdown client...")
    
    def buildProtocol(self, addr):
        return StandardApplicationComponent()


class StandardClientDevice():
    
    def __init__(self):
        self.canvas = None
        self.icon = None
        self.name = "Client"
        self.network_component = StandardClientNetworkComponent()

    def setCanvas(self, canvas):
        self.canvas = canvas

    def run(self):
        self.icon = VisualComponent(self.canvas, self.name, ICONS_PATH+"scinetsim_access_point.png", 100, 100)
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        
