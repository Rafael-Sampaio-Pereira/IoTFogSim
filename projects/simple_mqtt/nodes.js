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
            "coverage_area_radius": 0,
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
            "coverage_area_radius": 0,
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
            "coverage_area_radius": 0,
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
            "coverage_area_radius": 100,
            "application": "applications.mqttapp.PublisherApp",
            "x": 200,
            "y": 380
        },
        {
            "id": 4,
            "name": "Arduino based sensor (publisher node)", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": true,
            "coverage_area_radius": 100,
            "application": "applications.mqttapp.PublisherApp",
            "x": 300,
            "y": 380
        },
        {
            "id": 4,
            "name": "Arduino based sensor (publisher node)", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": true,
            "coverage_area_radius": 100,
            "application": "applications.mqttapp.PublisherApp",
            "x": 400,
            "y": 380
        },
        {
            "id": 4,
            "name": "Arduino based sensor (publisher node)", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": true,
            "coverage_area_radius": 100,
            "application": "applications.mqttapp.PublisherApp",
            "x": 500,
            "y": 380
        },
        {
            "id": 14,
            "name": "Arduino based sensor (publisher node)", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": true,
            "coverage_area_radius": 100,
            "application": "applications.mqttapp.PublisherApp",
            "x": 600,
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
            "coverage_area_radius": 100,
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
            "application": "applications.routerapp.RouterApp",
            "is_wireless": false,
            "coverage_area_radius": 0,
            "x": 400,
            "y": 200
        }
    ],
    "wireless_sensor_networks": [
        
    ]
}