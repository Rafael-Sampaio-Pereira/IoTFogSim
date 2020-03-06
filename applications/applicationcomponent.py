from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs
from scinetsim.standarddevice import Connection

from twisted.internet.task import LoopingCall

from multiprocessing import Process
import time

class StandardApplicationComponent(protocol.Protocol):
    
    def __init__(self):
        self.visual_component = None
        self.simulation_core =  None
        self.network_settings = None
        self.is_wireless = False
        self.wireless_signal_control_id = None

        
    def build_package(self, payload):
        package = {
                    "destiny_addr": self.destiny_addr,
                    "destiny_port": self.destiny_port,
                    "source_addr": self.source_addr,
                    "source_port": self.source_port,
                    "type": 'http',
                    "payload": payload
        }

        package = json.dumps(package)
        package = package
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        return msg_bytes


    def extract_package_contents(self, package):
        try:
            package = package.decode("utf-8")
            package = str(package)[0:]
            json_msg = json.loads(package)

            return json_msg["destiny_addr"], json_msg["destiny_port"], json_msg["source_addr"], json_msg["source_port"], json_msg["type"], json_msg["payload"]
        
        except Exception as e:
            log.msg(e)

    def update_alert_message_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="black")
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text=str(msg))

    def update_name_on_screen(self, msg):
        self.simulation_core.canvas.itemconfig(self.visual_component.draggable_name, text=str(msg))

    def connectionFailed(self, reason):
        log.msg('connection failed:', reason.getErrorMessage())
        self.simulation_core.updateEventsCounter("Connection failed")
    
    def connectionLost(self, reason):
        try:
            if self.simulation_core:
                log.msg('connection lost:', reason.getErrorMessage())
                self.simulation_core.updateEventsCounter("connection lost")
                self.simulation_core.allProtocols.remove(self)
        except NameError:
            log.msg("The requested simulation_core is no longer available")

    def send(self, message):
        self.transport.write(message+b"\n")

    def put_package_in_buffer(self, data):
        if data.endswith(b"\n"):
            packages = data.split(b"\n")
            for package in packages:
                if package != b'':
                    self._buffer.append(package)

    
    def save_protocol_in_simulation_core(self, proto):
        try:
            if self.simulation_core:
                if self.simulation_core:
                    self.simulation_core.allProtocols.add(proto)
                    #print(self.simulation_core.allProtocols)
            else:
                print("This divice have no simulation core instance")
        except NameError:
            log.msg("The requested simulation_core is no longer available")
        

    def create_connection_animation(self):
        # this method can only be called on the connectionMade method of the clients devices. do not use that in servers instances - Rafael Sampaio
        con = Connection(self.simulation_core, self, self.transport.getPeer().host, self.transport.getPeer().port)
        self.simulation_core.allConnections.add(con)
        

    # when the wifi access point executes the passive scanning metho, it is sending an beacon frame(in broadcast mode) for every device around it. - Rafael Sampaio
    def draw_wireless_signal(self, msg):
        
        if self.is_wireless == True:

            #log.msg("%s - Sending Wifi 802.11/* beacon broadcast message..."%(self.SSID))
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, fill="red")
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_alert, text="<< beacon >>")

            # setting the color of signal(circle border) from transparent to red. - Rafael Sampaio
            self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline="red")
            
            # The circle signal starts with raio 1 and propagates to raio 100. - Rafael Sampaio
            if self.visual_component.signal_radius > 0 and self.visual_component.signal_radius < self.visual_component.coverage_area_radius:
                # the ssignal radius propagates at 10 units per time. - Rafael Sampaio
                self.visual_component.signal_radius += 10
                self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y+self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)
                
                # Reactor will send a wiriless signal draw_wireless_signal  method at each 0.1024 s interval time. - Rafael Sampaio
                self.wireless_signal_control_id = reactor.callLater(0.1024, self.draw_wireless_signal, msg=msg)

            else:
                # Cleaning propagated signal for restore the signal draw. - Rafael Sampaio
                self.simulation_core.canvas.itemconfig(self.visual_component.draggable_signal_circle, outline = "")
                self.visual_component.signal_radius = 1

                self.wireless_signal_control_id.cancel()

            #self.simulation_core.canvas.update()
            
            
