import random

current_list = [{'name': 'DOOR_1', 'x': 684, 'y': 650}, {'name': 'DOOR_2', 'x': 560, 'y': 390}, {'name': 'DOOR_3', 'x': 380, 'y': 390}, {'name': 'POINT_1', 'x': 515, 'y': 610}, {'name': 'POINT_2', 'x': 385, 'y': 475}, {'name': 'POINT_3', 'x': 185, 'y': 470}, {'name': 'POINT_4', 'x': 190, 'y': 600}, {'name': 'POINT_5', 'x': 255, 'y': 205}, {'name': 'POINT_6', 'x': 570, 'y': 205}, {'name': 'BED', 'x': 410, 'y': 90}, {'name': 'SUPERMARKET', 'x': 950, 'y': 200}, {'name': 'WORKPLACE', 'x': 950, 'y': 643}]
print("THE CUR POINT IS: ", current_list)
current_list = [x for x in current_list if x['name'] != 'DOOR_2']
# current_list = list(set(current_list) - set(
# {
#     'name': 'DOOR_2',
#     'x': 560,
#     'y': 390
# }
# ))
print("THE NEW POINT IS: ", current_list)