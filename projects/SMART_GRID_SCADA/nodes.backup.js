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
                "application": "applications.smartgridapp.FogBrokerApp",
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
                "application": "applications.smartgridapp.SCADAApp",
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
                    },
                    {
                        "id": 3,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 957,
                        "y": 750
                    },
                    {
                        "id": 4,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1026,
                        "y": 1465
                    },
                    {
                        "id": 5,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 682,
                        "y": 1121
                    },
                    {
                        "id": 6,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 253,
                        "y": 820
                    },
                    {
                        "id": 7,
                        "name": "wsn_repeater",
                        "icon": "repeater_icon",
                        "coverage_area_radius": 207,
                        "is_wireless": true,
                        "application": "applications.wsnapp.RepeaterApp",
                        "x": 1028,
                        "y": 347
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
                    },
                    {
                        "id": 3,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 2068,
                        "y": 613
                    },
                    {
                        "id": 4,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 2087,
                        "y": 881
                    },
                    {
                        "id": 5,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1783,
                        "y": 847
                    },
                    {
                        "id": 6,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1862,
                        "y": 500
                    },
                    {
                        "id": 7,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1872,
                        "y": 419
                    },
                    {
                        "id": 8,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1824,
                        "y": 441
                    },
                    {
                        "id": 9,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1779,
                        "y": 485
                    },
                    {
                        "id": 10,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1867,
                        "y": 429
                    },
                    {
                        "id": 11,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1768,
                        "y": 429
                    },
                    {
                        "id": 12,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1732,
                        "y": 397
                    },
                    {
                        "id": 13,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1620,
                        "y": 357
                    },
                    {
                        "id": 14,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1474,
                        "y": 397
                    },
                    {
                        "id": 15,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1481,
                        "y": 474
                    },
                    {
                        "id": 16,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1478,
                        "y": 657
                    },
                    {
                        "id": 17,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1497,
                        "y": 1061
                    },
                    {
                        "id": 18,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1587,
                        "y": 1074
                    },
                    {
                        "id": 19,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1600,
                        "y": 1123
                    },
                    {
                        "id": 20,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1699,
                        "y": 1199
                    },
                    {
                        "id": 21,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1727,
                        "y": 1257
                    },
                    {
                        "id": 22,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1757,
                        "y": 1286
                    },
                    {
                        "id": 23,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1820,
                        "y": 1383
                    },
                    {
                        "id": 24,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1556,
                        "y": 1347
                    },
                    {
                        "id": 25,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1379,
                        "y": 746
                    },
                    {
                        "id": 26,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1355,
                        "y": 828
                    },
                    {
                        "id": 27,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1334,
                        "y": 667
                    },
                    {
                        "id": 28,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1312,
                        "y": 597
                    },
                    {
                        "id": 29,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1184,
                        "y": 541
                    },
                    {
                        "id": 30,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1247,
                        "y": 284
                    },
                    {
                        "id": 31,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1011,
                        "y": 181
                    },
                    {
                        "id": 32,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 819,
                        "y": 239
                    },
                    {
                        "id": 33,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 676,
                        "y": 55
                    },
                    {
                        "id": 34,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 818,
                        "y": 622
                    },
                    {
                        "id": 35,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1022,
                        "y": 879
                    },
                    {
                        "id": 36,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1137,
                        "y": 1110
                    },
                    {
                        "id": 37,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1340,
                        "y": 1043
                    },
                    {
                        "id": 38,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1066,
                        "y": 1087
                    },
                    {
                        "id": 39,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1004,
                        "y": 1129
                    },
                    {
                        "id": 40,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1050,
                        "y": 1335
                    },
                    {
                        "id": 41,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 1013,
                        "y": 1570
                    },
                    {
                        "id": 42,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 886,
                        "y": 1582
                    },
                    {
                        "id": 43,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 939,
                        "y": 1631
                    },
                    {
                        "id": 44,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 678,
                        "y": 835
                    },
                    {
                        "id": 45,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 677,
                        "y": 946
                    },
                    {
                        "id": 46,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 733,
                        "y": 950
                    },
                    {
                        "id": 47,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 746,
                        "y": 935
                    },
                    {
                        "id": 48,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 501,
                        "y": 902
                    },
                    {
                        "id": 49,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 375,
                        "y": 1152
                    },
                    {
                        "id": 50,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 489,
                        "y": 1181
                    },
                    {
                        "id": 51,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 526,
                        "y": 1234
                    },
                    {
                        "id": 52,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 596,
                        "y": 1284
                    },
                    {
                        "id": 53,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 619,
                        "y": 1259
                    },
                    {
                        "id": 54,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 320,
                        "y": 838
                    },
                    {
                        "id": 55,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 79,
                        "y": 792
                    },
                    {
                        "id": 56,
                        "name": "sensor",
                        "icon": "sensor_icon",
                        "coverage_area_radius": 207,
                        "application": "applications.wsnapp.SensorApp",
                        "is_wireless": true,
                        "x": 203,
                        "y": 1153
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