{
    "fog_nodes": [
        { 
            "name": "Fog Broker Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "server_icon",
            "type": "server",
            "is_wireless": false,
            "x": 250,
            "y": 175
        },
        { 
            "name": "Fog Storage Node ", 
            "simulation_ip": "192.121.0.2",
            "real_ip": "127.0.0.2",
            "icon": "server_icon",
            "type": "client",
            "is_wireless": true,
            "x": 500,
            "y": 175
        }
    ],
    "cloud_nodes": [
        {
            "name": "Cloud Computing Node", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "cloud_icon",
            "type": "server",
            "is_wireless": false,
            "x": 400,
            "y": 75
        }
    ],
    "iot_nodes": [
        {
            "name": "Arduino based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "arduino_uno_icon",
            "type": "client",
            "is_wireless": false,
            "x": 170,
            "y": 380
        },
        {
            "name": "ESP8266 based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "esp8266_icon",
            "type": "client",
            "is_wireless": false,
            "x": 370,
            "y": 440
        },
        {
            "name": "ESP8266 based sensor", 
            "simulation_ip": "192.121.0.1",
            "real_ip": "127.0.0.1",
            "icon": "esp8266_icon",
            "type": "client",
            "is_wireless": false,
            "x": 600,
            "y": 380
        }
    ],
    "access_points": [
        { 
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
            "website": "stackabuse.com", 
            "from": "Nebraska", 
            "name": "Scott",
            "is_wireless": "True"
        }
    ]
}