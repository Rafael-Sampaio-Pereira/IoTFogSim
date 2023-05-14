from tkinter import RIGHT
from twisted.internet import reactor
from twisted.internet import reactor
import os
import json

class SmartHomeAdapter(object):
    def __init__(self, simulation_core) -> None:
        print("Creating SmartHome adapter...")
        self.simulation_core = simulation_core
        self.ground_plan = SimpleGroundPlan(simulation_core)


class SimpleGroundPlan(object):
    """Ground Plan for simulate house envirioment in smart home context."""

    def __init__(self, simulation_core) -> None:
        self.simulation_core = simulation_core
        file_path = 'projects/'+simulation_core.project_name+'/ground_plan.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as ground_plan_file:
                data = json.loads(ground_plan_file.read())
                if data:
                    self.wall_tickness = data['wall_tickness']
                    self.wall_color = data['wall_color']
                    for wall in data['walls']:
                        self.draw_wall(
                            wall['start_x'],
                            wall['start_y'],
                            wall['end_point'],
                            wall['orientation']
                        )
        

    def draw_wall(self, start_x: int, start_y: int, end_point: int, orientation: str):
        if orientation not in ["v", "h"]:
            raise Exception(
                "Orientation field must be vertical or horizontal.")

        if orientation == "v":
            self.simulation_core.canvas.create_rectangle(start_x, start_y, start_x+self.wall_tickness, end_point,
                                                         fill=self.wall_color, width=1, tags=("wall",))
        else:
            self.simulation_core.canvas.create_rectangle(start_x, start_y, end_point, start_y+self.wall_tickness,
                                                         fill=self.wall_color, width=1, tags=("wall",))

    def blink_wall(self, wall):
        original_color = self.simulation_core.scene_adapter.ground_plan.wall_color
        self.simulation_core.canvas.itemconfig(wall, fill="red")
        reactor.callLater(
            0.7, self.simulation_core.canvas.itemconfig, wall, fill=original_color)

    def verify_wall_collision(self, x, y, tolerance):
        if not tolerance:
            tolerance = 0

        # finding all the wifi devices on the canvas screen
        all_wall = self.simulation_core.canvas.find_withtag("wall")
        collision_items = self.simulation_core.canvas.find_overlapping(
            x + tolerance,
            y + tolerance,
            x + tolerance,
            y + tolerance
        )

        for wall in all_wall:
            if wall in collision_items:
                self.blink_wall(wall)
                return True
        return False


# class PersonDataProducerApp(MobileProducerApp):
#     """
# #     This is based on in the MQTT MobileProducerApp.
# #     This Acts as a Publisher component send tasks to the 'task' mqtt topic.
# #     This generates MIPS task and send to OchesrtrationBrokerApp, so broker can
# #     send tasks to computeApps(Subscribers)
# #     """

#     # @override
#     def generate_data(self):
#         data = '{"coords": {"lat": 56.0000, "lng": 44.0000}}'
#         return data

#     # @override
#     def run_mobility(self):
#         # RandomWalkMobility(
#         #     self.visual_component,
#         #     self.simulation_core,
#         #     15
#         # )

#         RandomWaypointMobility(
#             self.visual_component,
#             self.simulation_core,
#             0.008,
#             0.02,
#             10,
#             100
#         )
        
#         # RandomDirectionMobility(
#         #     self.visual_component,
#         #     self.simulation_core,
#         #     0.008,
#         #     0.02,
#         #     10,
#         #     100
#         # )


# class PersonGraphDataProducerApp(PersonDataProducerApp):
#     # @override
#     def run_mobility(self):
#         GraphRandomWaypointMobility(
#             self.visual_component,
#             self.simulation_core,
#             0.008,
#             0.02,
#             10,
#             100
#         )
