
from twisted.internet import protocol, reactor,endpoints
from twisted.python import log
from utils.draggableImage import DraggableImage
import tkinter
from config.settings import ICONS_PATH


class StandardApplicationComponent(protocol.Protocol):
    def __init__(self, visual_component, canvas):
        self.visual_component = visual_component
        self.canvas = canvas

    def connectionMade(self):
        log.msg("One connection was successfuly established to %s"%(self.transport.getPeer().host+":"+str(self.transport.getPeer().port)))
        self.send(b"test data")
    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
    
    def connectionLost(self, reason):
        log.msg('connection lost:', reason.getErrorMessage())
    
    def send(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        # Print the received data on the sreen.  - Rafael Sampaio
        self.canvas.itemconfig(self.visual_component.draggable_alert, text=str(data)[1:])
        log.msg("Received data %s"%(data))




class VisualComponent(object):

    def __init__(self, canvas, deviceName, file, x, y):
        self.canvas = canvas
        self.image_file = tkinter.PhotoImage(file=file)
        self.draggable_img = self.canvas.create_image(x, y, image=self.image_file)

        self.draggable_name = self.canvas.create_text(x,y+27,fill="black",font="Arial 9",
                        text=deviceName)

        self.draggable_alert = self.canvas.create_text(x,y-27,fill="black",font="Times 9",
                        text="alert")
        # font="Times 9 italic bold"
         
        canvas.tag_bind(self.draggable_alert, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.draggable_alert, '<ButtonRelease-1>', self.release)
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

            self.canvas.move(self.draggable_alert,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)

            self.canvas.move(self.draggable_img,
                new_xpos-self.mouse_xpos ,new_ypos-self.mouse_ypos)
             
            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.draggable_img)
            self.canvas.tag_raise(self.draggable_name)
            self.canvas.tag_raise(self.draggable_alert)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y
 
    def release(self, event):
        self.move_flag = False


class StandardServerDevice():
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.visual_component = None
        self.name = "Server"
        self.visual_component = VisualComponent(self.canvas, self.name, ICONS_PATH+"scinetsim_restfull_server.png", 100, 100)
        #self.application_component = StandardApplicationComponent()
        self.network_component = StandardServerNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)
        #self.network_component.protocol = self.application_component

    def run(self):
        
        endpoints.serverFromString(reactor, self.network_component.network_settings).listen(self.network_component)



class StandardServerNetworkComponent():

    def __init__(self, host, port, visual_component, canvas):
        self.host = host
        self.port = port
        self.network_settings = "tcp:interface={}:{}".format(str(self.host),self.port)
        self.visual_component = visual_component
        self.canvas = canvas

    def doStart(self):
        log.msg("Initializing Server...")
    
    def doStop(self):
        log.msg("Shotdown Server...")
    
    def buildProtocol(self, addr):
        return StandardApplicationComponent(self.visual_component, self.canvas)


class StandardClientNetworkComponent():

    def __init__(self, serverHost, serverPort, visual_component, canvas):
        self.serverHost = serverHost
        self.serverPort = serverPort 
        self.network_settings = "tcp:{}:{}".format(self.serverHost,self.serverPort)
        self.visual_component = visual_component
        self.canvas = canvas

    def doStart(self):
        log.msg("Initializing client...")
    
    def doStop(self):
        log.msg("Shotdown client...")
    
    def buildProtocol(self, addr):
       return StandardApplicationComponent(self.visual_component, self.canvas)


class StandardClientDevice():
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.visual_component = None
        self.name = "Client"
        self.visual_component = VisualComponent(self.canvas, self.name, ICONS_PATH+"scinetsim_access_point.png", 100, 100)
        #self.application_component = StandardApplicationComponent()
        self.network_component = StandardClientNetworkComponent("127.0.0.1", 5000, self.visual_component, self.canvas)
        #self.network_component.protocol = self.application_component

    def run(self):
        
        client = endpoints.clientFromString(reactor, self.network_component.network_settings)
        client.connect(self.network_component)
        
