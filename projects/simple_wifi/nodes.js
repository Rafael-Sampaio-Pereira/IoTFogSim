{
    "fog": {
        "servers": [
            { 
                "id": 2,
                "name": "Web Server", 
                "simulation_ip": "192.121.0.1",
                "real_ip": "127.0.0.1",
                "icon": "broker_icon",
                "type": "server",
                "port": 8080,
                "is_wireless": false,
                "coverage_area_radius": 0,
                "application": "applications.httpapp.HttpServerApp",
                "x": 250,
                "y": 175
            }
        ],
        "clients":[],
        "wireless_computers": [
            {
                "id":0,
                "name": "notebook 1",
                "icon": "notebook_icon",
                "coverage_area_radius": 100,
                "application": "applications.wirelesscomputerapp.WirelessComputerApp",
                "is_wireless": true,
                "x": 400,
                "y": 370
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
                "coverage_area_radius": 0,
                "accesspoint_addr": "127.0.0.1",
                "accesspoint_port": 8082,
                "application": "applications.routerapp.RouterApp",
                "is_wireless": false,
                "x": 400,
                "y": 200,
                "access_points": [
                    { 
                        "id": 7,
                        "TBTT": 0.1024,
                        "SSID": "Rede privada 001",
                        "WPA2_password": "iotfogsim2019",
                        "icon": "ap_icon",
                        "coverage_area_radius": 200,
                        "application": "applications.accesspointapp.AccessPointApp",
                        "type": "access_point",
                        "is_wireless": true,
                        "x": 400,
                        "y": 300
                    }
                ]
            }
        ],
        "wireless_sensor_networks": []
    },
    
    "cloud": {
        "servers": [],
        "clients":[],
        "wireless_computers": [],
        "routers": [],
        "wireless_sensor_networks": []
    },

    "iot": {
        "servers": [],
        "clients":[],
        "wireless_computers": [],
        "routers": [],
        "wireless_sensor_networks": []
    }
}