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
                "application": "applications.pesquisaapp.FogDataReducitonBrokerApp",
                "x": 241,
                "y": 221
            }
        ],
        "clients":[
            { 
                "id": 1,
                "name": "SCADA System", 
                "simulation_ip": "192.121.0.1",
                "real_ip": "127.0.0.1",
                "icon": "cloud_icon",
                "type": "client",
                "is_wireless": false,
                "coverage_area_radius": 0,
                "application": "applications.wsnapp.SCADAApp",
                "x": 532,
                "y": 64
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
                "x": 535,
                "y": 217,
                "access_points": [
                    
                ]
            }
        ],

        "wireless_sensor_networks": [
            { 
                "id": 3,
                "name": "energy_metering_wsn", 
                "network_layer_protocol": "UDP",
                "application_layer_protocol": "Wi-SUN",
                "latency": "0.02",
                "wireless_standard": "IEEE_802.15.4g",
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
                        "coverage_area_radius": 250,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 975,
                        "y": 564
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 250,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 740,
                        "y": 497
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 250,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 815,
                        "y": 276
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 250,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1432,
                        "y": 1503
                    },
                    {
                        "id":0,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 250,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1675,
                        "y": 1760
                    }
                ],
                "sensor_nodes": [
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1368,
                        "y": 534
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1152,
                        "y": 391
                    },
                    
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1016,
                        "y": 827
                    },
                    
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 500,
                        "y": 600
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1632,
                        "y": 679
                    },

                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 294,
                        "y": 743
                    },

                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 596,
                        "y": 829
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1175,
                        "y": 1010
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1175,
                        "y": 1260
                    },
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1428,
                        "y": 978
                    }
                    ,
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1407,
                        "y": 1508
                    }
                    ,
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1685,
                        "y": 937
                    }
                    ,
                    {
                        "id":0,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 250,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1100,
                        "y": 1492
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