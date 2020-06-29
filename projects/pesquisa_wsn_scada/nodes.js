{
    "fog": {
        "servers": [
            { 
                "id": 1,
                "name": "Fog Broker Node", 
                "simulation_ip": "192.121.0.1",
                "real_ip": "127.0.0.1",
                "icon": "broker_icon",
                "type": "server",
                "port": 5100,
                "is_wireless": false,
                "coverage_area_radius": 0,
                "application": "applications.mqttapp.BrokerApp",
                "x": 250,
                "y": 175
            }
        ],
        "clients":[
            { 
                "id": 1,
                "name": "SCADA System", 
                "simulation_ip": "192.121.0.1",
                "real_ip": "127.0.0.1",
                "icon": "notebook_icon",
                "type": "client",
                "is_wireless": false,
                "coverage_area_radius": 0,
                "application": "applications.wsnapp.SCADAApp",
                "x": 582,
                "y": 67
            }
        ],
        "wireless_computers": [],
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
                        "id":0,
                        "name": "wsn_sink",
                        "icon": "sink_icon",
                        "coverage_area_radius": 100,
                        "is_wireless": true,
                        "application": "applications.wsnapp.SinkApp",
                        "x": 1212,
                        "y": 216
                    }
                ],
                "repeater_nodes": [
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 150,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 975,
                        "y": 564
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 150,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 740,
                        "y": 497
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 150,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 815,
                        "y": 276
                    }
                ],
                "sensor_nodes": [
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1168,
                        "y": 291
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 850,
                        "y": 200
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1152,
                        "y": 391
                    },
                    
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1133,
                        "y": 487
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 617,
                        "y": 604
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 624,
                        "y": 510
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 870,
                        "y": 680
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 887,
                        "y": 591
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 100,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 780,
                        "y": 410
                    }
                ]
            }
        ]
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