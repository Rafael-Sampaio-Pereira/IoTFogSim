{
    "fog_nodes": [
        { 
            "id": 1,
            "name": "Fog Broker Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "server",
            "is_wireless": false,
            "application": "applications.mqttapplicationcomponent.BrokerApplicationComponent",
            "x": 250,
            "y": 175
        }
    ],
    "cloud_nodes": [
        
    ],
    "iot_nodes": [
        {
            "id": 4,
            "name": "Arduino based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": false,
            "application": "applications.mqttapplicationcomponent.PublisherApplicationComponent",
            "x": 170,
            "y": 380
        }
    ],
    "access_points": [
        
    ],
    "routers": [
        { 
            "id": 8,
            "name": "Router 001", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "router_icon",
            "type": "router",
            "port": 8081,
            "application": "applications.routerapplicationcomponent.RouterApplication",
            "is_wireless": false,
            "x": 400,
            "y": 200
        }
    ]
}