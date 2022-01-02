



iconsList = {

	"ap_icon": "iotfogsim_access_point.png",
	"ap_signal_icon": "iotfogsim_access_point_signal.png",
	"application_server_icon": "iotfogsim_application_server.png",
	"arduino_uno_icon": "iotfogsim_arduino_uno.png",
	"arduino_uno_signal_icon": "iotfogsim_arduino_uno_signal.png",
	"broker_icon": "iotfogsim_broker.png",
	"car_icon": "iotfogsim_car.png",
	"client_icon": "iotfogsim_client.png",
	"cloud_icon": "iotfogsim_cloud.png",
	"database_server_icon": "iotfogsim_database_server.png",
	"esp8266_icon": "iotfogsim_esp8266.png",
	"esp8266_signal_icon": "iotfogsim_esp8266_signal.png",
	"internet_icon": "iotfogsim_internet.png",
	"notebook_icon": "iotfogsim_notebook.png",
	"repeater_icon": "iotfogsim_repeater.png",
	"restfull_server_icon": "iotfogsim_restfull_server.png",
	"router_icon": "iotfogsim_router.png",
	"server_icon": "iotfogsim_server.png",
	"sensor_icon": "iotfogsim_sensor_node.png",
	"sensor_signal_icon": "iotfogsim_sensor_node_signal.png",
	"sink_icon": "iotfogsim_sink.png",
	"small_current_sensor_icon": "iotfogsim_small_current_sensor.png",
	"smart_meter_icon": "iotfogsim_smart_meter.png",
	"smart_meter_icon_signal": "iotfogsim_smart_meter_signal.png",
	"smartphone_icon": "iotfogsim_smartphone.png",

}


def getIconFileName(icon_name):
	for icon in iconsList:
	    if icon == icon_name:
	    	return iconsList[icon]


def getIconName(file_name):
    for icon_name , icon_path in iconsList.items():
	    if icon_path == file_name:
	    	return icon_name
