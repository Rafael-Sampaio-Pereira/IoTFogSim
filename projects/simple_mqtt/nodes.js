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
            "id": 2,
            "name": "Fog Broker Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "server",
            "port": 5000,
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
            "is_wireless": false,
            "application": "applications.mqttapp.PublisherApp",
            "x": 170,
            "y": 380
        }
    ],
    "access_points": [
        
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
            "x": 400,
            "y": 200
        }
    ]
}