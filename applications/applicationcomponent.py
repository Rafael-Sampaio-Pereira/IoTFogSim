from twisted.internet import protocol, reactor
from twisted.python import log
import json
import codecs
from core.standarddevice import Connection

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
        self.name = None

    def connectionMade(self):
        self.transport.logstr = '-'

    def build_package(self, payload, type):
        package = {
                    "destiny_addr": self.destiny_addr,
                    "destiny_port": self.destiny_port,
                    "source_addr": self.source_addr,
                    "source_port": self.source_port,
                    "type": type,
                    "payload": payload
        }

        package = json.dumps(package)
        msg_bytes, _ = codecs.escape_decode(package, 'utf8')
        return msg_bytes


    def extract_package_contents(self, package):
        try:
            package = package.decode("utf-8")
            package = str(package)[0:]

            #####################################################################################
            # ESTES TRATAMENTOS SÃO PROVISORIOS ENQUANTO OS DISPOSITIVOS BASEADOS EM TWISTED NÃO #
            # ESTÃO ARMAZENADNO OS DADOS RECEBIDOS EM UM BUFFER 23/06/2020 - Rafael Sampaio     #
            #####################################################################################

            # this was add because mqtt application has detected two json objects in one packages and these was not sparated by comma - Rafael Sampaio
            if "}{" in package:
                packages = package.replace("}{","},{")

                packages = json.dumps(packages)
                print("MQTT - um pacote vai ser dropado, infelizmente ", packages)
                # print(packages[0])
                json_msg = json.loads(packages[0])

            # this was add because the wsn sink has send data and router has received the sent data grouped in a single line - Rafael Sampaio
            if "}}\n{" in package:
                
                packages = package.split("\n")
                
                print("TCP - um ou mais pacotes vão ser dropados, infelizmente ")
            
                json_msg = json.loads(packages[0])
             
            else:
                json_msg = json.loads(package)

            return json_msg["destiny_addr"], json_msg["destiny_port"], json_msg["source_addr"], json_msg["source_port"], json_msg["type"], json_msg["payload"]
        
        except Exception as e:
            print('CAIU AQUI')
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
        if self.transport:
            self.transport.write(message+b"\n")
        else:
            decripition = (self.name if self.name else str(type(self).__name__))
            log.msg("Info : - | %s - Unknow Device trying to send message, but the protocol is not connected"%decripition)

    def put_package_in_buffer(self, data):
        if data.endswith(b"\n"):
            packages = data.split(b"\n")
            for package in packages:
                if package != b'':
                    self._buffer.append(package)

    def save_protocol_in_simulation_core(self, proto, message=None):
        try:
            if self.simulation_core:
                if self.simulation_core:
                    self.simulation_core.allProtocols.add(proto)
                    #print(self.simulation_core.allProtocols)
            else:
                decripition = self.name if self.name else str(type(self).__name__)
                if message:
                    log.msg("Info : - | %s This divice have no simulation core instance - TRACK MESSAGE: "+str(message)%decripition)
                else:
                    log.msg("Info : - | %s This divice have no simulation core instance"%decripition)
        except NameError:
            log.msg("The requested simulation_core is no longer available")

    def create_connection_animation(self):
        # this method can only be called on the connectionMade method of the clients devices. do not use that in servers instances - Rafael Sampaio
        con = Connection(self.simulation_core, self, self.transport.getPeer().host, self.transport.getPeer().port)
        self.simulation_core.allConnections.add(con)

