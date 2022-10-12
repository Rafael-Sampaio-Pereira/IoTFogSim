from apps.base_app import BaseApp


class SmartTVApp(BaseApp):
    def __init__(self):
        super(SmartTVApp, self).__init__()
        self.name = 'SmartTVApp'
        
        
#         {
#     "name": "router1 <----------> router2",
#     "bandwidth": 256,
#     "packet_loss_rate": 0.10,
#     "network_interface_1": "10.10.0.1",
#     "network_interface_2": "10.10.0.2",
#     "delay_upper_bound": 200,
#     "delay_lower_bound": 60,
#     "delay_mean": 70,
#     "delay_standard_deviation": 10
# },