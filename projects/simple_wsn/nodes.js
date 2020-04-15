{
    "fog_nodes": [
        { 
            "id": 1,
            "name": "Fog Subscriber Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "client",
            "is_wireless": false,
            "application": "applications.mqttapp.SubscriberApp",
            "x": 550,
            "y": 175
        },
        { 
            "id": 1,
            "name": "Fog Subscriber Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "client",
            "is_wireless": false,
            "application": "applications.mqttapp.SubscriberApp",
            "x": 400,
            "y": 75
        },
        { 
            "id": 2,
            "name": "Fog Broker Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "server",
            "port": 5100,
            "is_wireless": false,
            "application": "applications.mqttapp.BrokerApp",
            "x": 250,
            "y": 175
        }
    ],
    "cloud_nodes": [
        
    ],
    "iot_nodes": [
        {
            "id": 4,
            "name": "Arduino based sensor (publisher node)", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": true,
            "application": "applications.mqttapp.PublisherApp",
            "x": 200,
            "y": 380
        }
    ],
    "access_points": [
        { 
            "id": 7,
            "TBTT": 0.1024,
            "SSID": "Rede privada 001",
            "WPA2_password": "iotfogsim2019",
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "port": 8082,
            "icon": "ap_icon",
            "router_addr": "127.0.0.1",
            "router_port": 8081,
            "application": "applications.accesspointapp.AccessPointApp",
            "type": "access_point",
            "is_wireless": true,
            "x": 400,
            "y": 300
        }
    ],
    "routers": [
        { 
            "id": 3,
            "name": "Router 001", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "router_icon",
            "type": "router",
            "port": 8081,
            "accesspoint_addr": "127.0.0.1",
            "accesspoint_port": 8082,
            "application": "applications.routerapp.RouterApp",
            "is_wireless": false,
            "x": 400,
            "y": 200
        }
    ],
    "wireless_sensor_networks": [
        { 
            "id": 3,
            "name": "energe_metering_wsn", 
            "ip_standard": "6LowPan",
            "network_layer_protocol": "UDP",
            "wireless_standard": "IEEE_802.11",
            "description": "Simple wsn for envirioment monitoring",
            "sink_nodes": [
                {
                    "id":20,
                    "name": "wsn_sink",
                    "icon": "sensor_signal_icon",
                    "is_wireless": true,
                    "application": "applications.wsnapp.SinkApp",
                    "x": 750,
                    "y": 100
                }
            ],
            "sensor_nodes": [
                {
                    "id":20,
                    "name": "wsn_sensor",
                    "icon": "sensor_icon",
                    "application": "applications.wsnapp.SensorApp",
                    "is_wireless": true,
                    "x": 750,
                    "y": 200
                },
                {
                    "id":20,
                    "name": "wsn_sensor",
                    "icon": "sensor_icon",
                    "application": "applications.wsnapp.SensorApp",
                    "is_wireless": true,
                    "x": 750,
                    "y": 300
                }
            ]
        }
    ]
}