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
            "application": "applications.applicationcomponent.StandardServerApplicationComponent",
            "x": 250,
            "y": 175
        },
        {   
            "id": 2,
            "name": "Fog Storage Node ", 
            "simulation_ip": "192.121.0.2",
            "real_ip": "127.0.0.2",
            "icon": "server_icon",
            "type": "client",
            "is_wireless": true,
            "application": "applications.applicationcomponent.StandardServerApplicationComponent",
            "x": 500,
            "y": 175
        }
    ],
    "cloud_nodes": [
        {
            "id": 3,
            "name": "Cloud Computing Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "cloud_icon",
            "type": "server",
            "is_wireless": false,
            "application": "applications.applicationcomponent.StandardServerApplicationComponent",
            "x": 400,
            "y": 75
        }
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
            "application": "applications.applicationcomponent.StandardClientApplicationComponent",
            "x": 170,
            "y": 380
        },
        {
            "id": 5,
            "name": "ESP8266 based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "esp8266_icon",
            "type": "client",
            "is_wireless": false,
            "application": "applications.applicationcomponent.StandardClientApplicationComponent",
            "x": 370,
            "y": 440
        },
        {
            "id": 6,
            "name": "ESP8266 based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "esp8266_icon",
            "type": "client",
            "is_wireless": false,
            "application": "applications.applicationcomponent.StandardClientApplicationComponent",
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
            "icon": "ap_icon",
            "type": "access_point",
            "is_wireless": true,
            "x": 400,
            "y": 300
        }
    ],
    "routers": [
        { 
            "id": 8,
            "name": "Router 001", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "router_icon",
            "type": "router",
            "is_wireless": false,
            "x": 400,
            "y": 200
        }
    ]
}