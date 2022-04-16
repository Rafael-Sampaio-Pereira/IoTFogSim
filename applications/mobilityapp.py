
from core.dataproducers import *
from core.mobiledevice import BaseStationNode
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.python import log
import twisted
import time
import uuid
import json
import tkinter as tk
from applications.applicationcomponent import StandardApplicationComponent
from core.functions import create_csv_database_file
from twisted.internet.task import LoopingCall
from datetime import datetime
from applications.mqttapp import extract_mqtt_contents
import random
from bresenham import bresenham


class MobileNodeApp(StandardApplicationComponent):
    # This class is originated from the WSNApp, so new implementations are made to
    # turn computational node to be mobile. This class can be used to create any mobile node such as
    # vehicular node or smartphone. Gateway are based on a new class called BaseStation - Rafael Sampaio
    def __init__(self):
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        # self.nearby_devices_list = None

    def show_signal(self):
        self.visual_component.signal_radius = self.visual_component.coverage_area_radius
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline="red")
        self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle,
                                           self.visual_component.x+self.visual_component.signal_radius,
                                           self.visual_component.y+self.visual_component.signal_radius,
                                           self.visual_component.x-self.visual_component.signal_radius,
                                           self.visual_component.y-self.visual_component.signal_radius)

    def set_signal_radius(self, radius):
        self.visual_component.signal_radius = radius
        self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y +
                                           self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)

    def clear_signal_radius(self, radius):
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline="")
        self.visual_component.signal_radius = radius
        self.simulation_core.canvas.coords(self.visual_component.draggable_signal_circle, self.visual_component.x+self.visual_component.signal_radius, self.visual_component.y +
                                           self.visual_component.signal_radius, self.visual_component.x-self.visual_component.signal_radius, self.visual_component.y-self.visual_component.signal_radius)

    def _blink_signal(self):
        self.simulation_core.canvas.itemconfig(
            self.visual_component.draggable_signal_circle, outline="red")
        self.simulation_core.canvas.after(
            15, self.set_signal_radius, self.visual_component.coverage_area_radius/10)
        self.simulation_core.canvas.after(
            25, self.set_signal_radius, self.visual_component.coverage_area_radius/9)
        self.simulation_core.canvas.after(
            35, self.set_signal_radius, self.visual_component.coverage_area_radius/8)
        self.simulation_core.canvas.after(
            45, self.set_signal_radius, self.visual_component.coverage_area_radius/7)
        self.simulation_core.canvas.after(
            55, self.set_signal_radius, self.visual_component.coverage_area_radius/6)
        self.simulation_core.canvas.after(
            65, self.set_signal_radius, self.visual_component.coverage_area_radius/5)
        self.simulation_core.canvas.after(
            75, self.set_signal_radius, self.visual_component.coverage_area_radius/4)
        self.simulation_core.canvas.after(
            85, self.set_signal_radius, self.visual_component.coverage_area_radius/3)
        self.simulation_core.canvas.after(
            95, self.set_signal_radius, self.visual_component.coverage_area_radius/2)
        self.simulation_core.canvas.after(
            105, self.set_signal_radius, self.visual_component.coverage_area_radius)
        self.simulation_core.canvas.after(200, self.clear_signal_radius, 0)

    # def print_node_connections(self, nearby_devices_list):
    #     self_name = self.simulation_core.canvas.itemcget(
    #         self.visual_component.draggable_name, 'text')
    #     print("=========", self_name, "==========")
    #     if len(nearby_devices_list) > 0:
    #         for nearby_device in nearby_devices_list:
    #             device_name = self.simulation_core.canvas.itemcget(
    #                 nearby_device.application.visual_component.draggable_name, 'text')
    #             if self_name != device_name:
    #                 print(self_name, ' <-------> ', device_name)
    #     print("=============================")
    #     print('\n')

    def print_node_buffer(self):
        self_name = self.simulation_core.canvas.itemcget(
            self.visual_component.draggable_name, 'text')
        buffer_string = ''
        for package in self._buffer:
            buffer_string += '|'+str(package.data)
        print(self_name, buffer_string)
        print('\n')

    def draw_connection_arrow(self, destiny):
        self._blink_signal()
        x1 = self.visual_component.x
        y1 = self.visual_component.y
        x2 = destiny.visual_component.x
        y2 = destiny.visual_component.y
        connection_id = self.simulation_core.canvas.create_line(
            x1, y1, x2, y2, arrow=tk.LAST, width=2, dash=(4, 2))

        self.simulation_core.canvas.after(
            5, self.delete_connection_arrow, connection_id)
        # reactor.callLater(0.3, self.delete_connection_arrow, connection_id)
        self.simulation_core.canvas.update()
        # return connection_id

        self.ball = self.simulation_core.canvas.create_oval(
            x1, y1, x1+7, y1+7, fill="red")
        self.all_coordinates = list(bresenham(x1, y1, x2, y2))
        # time that the packege ball still on the screen after get the destinantion - Rafael Sampaio
        self.display_time = 9
        # this must be interger and determines the velocity of the packet moving in the canvas - Rafael Sampaio
        self.package_speed = 1

        self.animate_package(x2, y2)

    def animate_package(self, destiny_x, destiny_y):
        cont = 100
        for x, y in self.all_coordinates:
            # verify if package ball just got its destiny - Rafael Sampaio
            if x == destiny_x and y == destiny_y:
                self.simulation_core.canvas.after(
                    cont+self.display_time, self.simulation_core.canvas.delete, self.ball)

            # 7 is the package ball size - Rafael Sampaio
            self.simulation_core.canvas.after(
                cont, self.simulation_core.canvas.coords, self.ball, x, y, x+7, y+7)
            cont = cont + self.package_speed

    def delete_connection_arrow(self, id):
        self.simulation_core.canvas.delete(id)
        self.simulation_core.canvas.update()

    def simulate_network_latency(self):
        time.sleep(
            float(self.visual_component.device.mobile_network_group.latency))

    def run_random_mobility(self):
        def move():
            # moving the device icon in canvas in random way - Rafael Sampaio
            direction = random.randint(1, 4)
            reference = random.randint(1, 100)

            if direction == 1:  # up
                if not (self.visual_component.y - reference) < 1:
                    self.visual_component.y = self.visual_component.y - reference
            elif direction == 2:  # down
                if not (self.visual_component.y + reference) > self.simulation_core.canvas.winfo_height():
                    self.visual_component.y = self.visual_component.y + reference
            elif direction == 3:  # left
                if not (self.visual_component.x - reference) < 1:
                    self.visual_component.x = self.visual_component.x - reference
            elif direction == 4:  # right
                if not (self.visual_component.x + reference) > self.simulation_core.canvas.winfo_width():
                    self.visual_component.x = self.visual_component.x + reference

            if self.visual_component.is_wireless:
                self.simulation_core.canvas.moveto(self.visual_component.draggable_coverage_area_circle,
                                                   self.visual_component.x, self.visual_component.y)

                self.simulation_core.canvas.moveto(self.visual_component.draggable_signal_circle,
                                                   self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_name,
                                               self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_alert,
                                               self.visual_component.x, self.visual_component.y)

            self.simulation_core.canvas.moveto(self.visual_component.draggable_img,
                                               self.visual_component.x, self.visual_component.y)

        LoopingCall(move).start(0.1)


class MobileProducerApp(MobileNodeApp):
    """
    Acts as publish mqtt node - Rafael Sampaio
    """
    def __init__(self):
        self._buffer = set()
        self.interval = 5.0
        self.simulation_core = None
        self.visual_component = None
        # self.nearby_devices_list = None
        self.connected_basestations = set()
        self.mobile_network_group = None


    def find_nearby_devices_icon(self):
        # getting all canvas objects in wireless signal coverage area - Rafael Sampaio
        all_coveraged_devices = self.simulation_core.canvas.find_overlapping(
            self.visual_component.x+self.coverage_area_radius,
            self.visual_component.y+self.coverage_area_radius,
            self.visual_component.x-self.coverage_area_radius,
            self.visual_component.y-self.coverage_area_radius)
        return all_coveraged_devices


    def connect_to_nearby_basesatation(self):
        # TO DO: needs to implement authorization and autetication methods for wireless tecnology such as 5g and wifi - Rafael Sampaio
        # TO DO: needs to implement a disconect function to lose conection when node are far of basestation - Rafael Sampaio

        # putting all nearby devices icons in a list that will be use in future to send data across - Rafael Sampaio
        nearby_devices_icon_list = self.find_nearby_devices_icon()


        for icon_id in nearby_devices_icon_list:
            device = self.mobile_network_group.get_mobile_network_device_by_icon(
                icon_id)
            if type(device) == BaseStationNode and device not in self.connected_basestations:
                self.simulation_core.updateEventsCounter("Mobile producer "+self.name+" connected to the Basestantion "+device.name)
                self.connected_basestations.add(device)

    def start(self):
        self.name = self.simulation_core.canvas.itemcget(
            self.visual_component.draggable_name, 'text')
        # self.nearby_devices_list = nearby_devices_list
        # self.print_node_connections(nearby_devices_list)
        LoopingCall(self.connect_to_nearby_basesatation).start(2.0)

        LoopingCall(self.collect_data).start(self.interval)
        # all sensors forward/routes packages every seconds. its not data collection interval - Rafael Sampaio
        LoopingCall(self.forward_packages).start(1.0)
        self.run_random_mobility()

    def generate_data(self):
        speed = '20km'
        coord = ['10', '15']
        data = '{"speed": "'+speed+'", "x": "' + \
            coord[0]+'", "y": "'+coord[1]+'"}'
        return data

    def collect_data(self):
        # Default data collection are made about veichulat mensurements.
        # User can change this method to retun any simulated values.
        # Data needs to be in JSON object stuct(i.e. Key-value) - Rafael Sampaio

        # Creating a new package - Rafael Sampaio
        pack = MobilePackage(source=self, data=self.generate_data())

        # putting this device in the generated package trace - Rafael Sampaio
        pack.put_in_trace(self)

        # putting data in device buffer - Rafael Sampaio
        self._buffer.add(pack)


    def forward_packages(self):
        def remove_sent_packages_from_buffer(_package):
            # after send, remove data from buffer - Rafael Sampaio
            self._buffer.remove(_package)

        if len(self._buffer) > 0:
            self.temp_buffer = self._buffer.copy()

            # sending each data in buffer for all devices arround via broadcast- Rafael Sampaio
            for _package in self.temp_buffer:
                self.forward_package(_package)
                remove_sent_packages_from_buffer(_package)

    def forward_package(self, package):

        if len(package.trace) > 0:
            # self._blink_signal()
            for destiny in self.connected_basestations:
                if destiny == package.source:
                    # A device can not sent data to it self - Rafael Sampaio
                    pass
                elif package.verify_if_device_is_in_trace(destiny):
                    # The package will not be send to devices that already in the package trace - Rafael Sampaio
                    pass
                else:
                    # Veryfing if the package already in the buffer (the nearby devices can send data back and its duplicates package in the buffer) - Rafael Sampaio
                    if not package in destiny.application._buffer:
                        # Drawing connection - Rafael Sampaio
                        reactor.callFromThread(
                            self.draw_connection_arrow, destiny)
                        self.simulation_core.canvas.update()

                        # self.simulate_network_latency()

                        package_id = json.loads(package.get_package_as_json())['id']
                        print()
                        # puting package in destiny device buffer - Rafael Sampaio
                        destiny.application._buffer.add(package)
                        package.put_in_trace(destiny)

                        self.simulation_core.updateEventsCounter(
                            "%s --> Mobile data producer node send data - message id: %s"%(self.name,package_id))


class BaseStationApp(MobileNodeApp):
    """
    Acts as concentrator mqtt node - Rafael Sampaio
    """
    def __init__(self):
        # this buffer stores only data from the mobile data producer - Rafael Sampaio
        self._buffer = set()
        self.simulation_core = None
        self.visual_component = None
        self.base_station_factory = None
        self.gateway_addr = '127.0.0.1'
        self.gateway_port = 8081
        # Destiny info (e.g. mqtt based server addr and port) - Rafael Sampaio
        self.destiny_addr = '127.0.0.1'
        self.destiny_port = 5100
        self.source_addr = None
        self.source_port = None
        self.mqtt_destiny_topic = None

    def start(self):
        self.connect_to_gateway()
        self.configure_source_info()

    # this method allow the BaseStation to connect to router/switch - Rafael Sampaio
    def connect_to_gateway(self):
        # get start to connect to gateway - Rafael Sampaio
        factory = BaseStationAppFactory(
            self.simulation_core, self.visual_component)
        factory.noisy = False
        reactor.connectTCP(self.gateway_addr, self.gateway_port, factory)
        self.base_station_factory = factory

    def configure_source_info(self):
        # get the network info from the base station protocol and using it to set the base station app network info - Rafael Sampaio
        if self.base_station_factory:
            if self.base_station_factory.running_protocol:
                if not self.source_addr:
                    self.source_addr = self.base_station_factory.running_protocol.source_addr

                if not self.source_port:
                    self.source_port = self.base_station_factory.running_protocol.source_port

        # while the source info is not complete this function will be recursivelly called - Rafael Sampaio
        if self.source_addr == None or self.source_port == None:
            reactor.callLater(1, self.configure_source_info)
        else:
            # the base station only starts to forward packages after connect to a router/gateway and get an network configurantion - Rafael Sampaio
            # forwarding packages every 'x' secondes - Rafael Sampaio
            LoopingCall(self.forward_packages).start(30.0)

    def forward_packages(self):
        if self.verify_buffer():
            if self.base_station_factory.running_protocol and (self.source_addr != None and self.source_port != None):
                data = "["
                # forwarding packages to the gateway - Rafael Sampaio
                for mobile_package in self._buffer.copy():

                    data += '{ "id": "' + str(mobile_package.id) + '", "source": "' + mobile_package.source.name + \
                        '", "data": ' + mobile_package.data + \
                            ', "created_at": "' + mobile_package.created_at + '" },'
                    self._buffer.remove(mobile_package)

                data = data[:-1]
                data += "]"

                data = json.loads(data)

                # this method is work into a mqtt context. to execute another scenario, pelase, change this method - Rafael Sampaio
                mqtt_msg = {
                    "action": "publish",
                    "topic": self.mqtt_destiny_topic,
                    "content": data
                }

                mqtt_package = self.build_package(mqtt_msg, 'mqtt')

                # this uses the send method defined in the StandardApplicationComponent class - Rafael Sampaio
                self.base_station_factory.running_protocol.send(mqtt_package)

    def verify_buffer(self):
        if len(self._buffer) > 0:
            return True
        else:
            return False


class BaseStationAppFactory(ClientFactory):

    def __init__(self, simulation_core, visual_component):
        self.running_protocol = None
        self.visual_component = visual_component
        self.simulation_core = simulation_core

    def buildProtocol(self, address):
        self.running_protocol = BaseStationAppProtocol(
            self.simulation_core, self.visual_component)
        self.running_protocol.save_protocol_in_simulation_core(
            self.running_protocol)
        return self.running_protocol


# this protocol acts as a client to the router/switch - Rafael Sampaio
class BaseStationAppProtocol(StandardApplicationComponent):

    def __init__(self, simulation_core, visual_component):
        self.visual_component = visual_component
        self.simulation_core = simulation_core
        self._buffer = set()  # this base station uses only one buffer, you need to pay atention when your application has top-down approachs - Rafael Sampaio
        # the base station network info will be generated after the connection to a gateway such as router or switch - Rafael Sampaio
        self.source_addr = None
        self.source_port = None

    def connectionMade(self):
        self.source_addr = self.transport.getHost().host
        self.source_port = self.transport.getHost().port
        self.transport.setTcpKeepAlive(1)
        self.terminateLater = None
        self.create_connection_animation()

    # This method is overhidding the dataReceived method in the StandardApplicationComponent class - Rafael Sampaio
    def dataReceived(self, data):
        # this base station uses the bottom-up approach and dont let us to use top-down messages/commands - Rafael Sampaio
        pass

    def connectionLost(self, reason):
        pass

    def write(self, data):
        if data:
            self.transport.write(data)


class MobilePackage(object):

    def __init__(self, source,  data):
        self.id = uuid.uuid4().fields[-1]
        self.source = source
        # self.destiny = destiny
        self.data = data
        #self.was_forwarded = False
        self.trace = set()
        self.created_at = datetime.now().isoformat()

    def get_package_as_json(self):
        package = {
            "id": str(self.id),
            "source": self.source.name,
            "data": json.loads(self.data),
            "created_at": self.created_at
        }

        package = json.dumps(package)

        return package

    def put_in_trace(self, device):
        device_name = self.source.simulation_core.canvas.itemcget(
            device.visual_component.draggable_name, 'text')
        self.trace.add(device_name)

    def verify_if_device_is_in_trace(self, device):
        device_name = self.source.simulation_core.canvas.itemcget(
            device.visual_component.draggable_name, 'text')
        if device_name in self.trace:
            return True
        else:
            return False

    def print_trace(self):
        src = self.source.simulation_core.canvas.itemcget(
            self.source.visual_component.draggable_name, 'text')
        trace_string = str(self.id)+": "+src

        for device in self.trace:
            if not device == src:
                trace_string += " - "+device
        print(trace_string)
