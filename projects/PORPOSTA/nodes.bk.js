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
                "application": "applications.researchapp.FogDataReducitonBrokerApp",
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
                "application": "applications.researchapp.SCADAResearchApp",
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
                        "id": 1,
                        "name": "wsn_sink",
                        "icon": "sink_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.SinkApp",
                        "x": 2305,
                        "y": 538
                    }
                ],
                "repeater_nodes": [
                    {
                        "id": 1,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1951,
                        "y": 770
                    },
                    {
                        "id": 2,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1364,
                        "y": 368
                    }
                ],
                "sensor_nodes": [
                    {
                        "id": 1,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 2192,
                        "y": 456
                    },
                    {
                        "id": 2,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 2121,
                        "y": 621
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