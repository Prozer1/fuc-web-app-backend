import math, datetime

def add_value_to_map(map, values, drone_number, mission_id, sensors = False):
    """
    Utils function to add values to DB map.
    
    Args:
        map: the dict where all the coordinates / drone info are store.
        values: list of coordinates to add to the map.
        drone_number: the drone number map to edit.
        mission_id: the mission id to add value to.
        sensors: (Optional) update the drone_sensors map and not the drone map.
    Returns:
        The edited map.
    """
    new_set = {}
    for key, value in map.items():
        if sensors:
            if f'drone_{drone_number}_sensors' == key:
                higher_int = get_biggest_int(value) + 1
                for sensors_data in values:
                    new_set[f'map/drone_{drone_number}_sensors/data_{higher_int}'] = {
                        "x": sensors_data[0], "y":sensors_data[1]
                        }
                    higher_int += 1
        else:
            if f'drone_{drone_number}' == key:
                higher_int = get_biggest_int(value) + 1
                new_set[f'map/drone_{drone_number}/x_{higher_int}'] = values[0]
                new_set[f'map/drone_{drone_number}/y_{higher_int}'] = values[1]
                new_set[f'map/drone_{drone_number}/x_current'] = values[0]
                new_set[f'map/drone_{drone_number}/y_current'] = values[1]
    return new_set

def update_local_map(map, firebase_payload):
    """Dictionnary update for local map. (not on firebase)

    Args:
        map (dict): The map stored in Drone objects
        firebase_payload (dict): group of key values but key are like 'main/child_node/child_node/value_to_change'

    Returns:
        dict: The edited map.
    """
    for key, value in firebase_payload.items():
        splited_key = key.split('/')
        tmp_map = map
        if splited_key:    
            for item in splited_key:
                if item == 'map':
                    continue
                if item == splited_key[-1]:
                    tmp_map[item] = value
                tmp_map = tmp_map[item]
    return map
    
def get_biggest_int(dictionnary):
    """
    Utils function return the biggest int from a list of keys in a dict.
    
    Args:
        dictionnary: the dict where are stored the keys.
    Returns:
        The biggest int.
    """
    higher_int = 0
    for key, value in dictionnary.items():
        extracted_int = [int(s) for s in key.split('_') if s.isdigit()]
        if extracted_int != []:
            if extracted_int[0] > higher_int:
                higher_int = extracted_int[0]
    return higher_int

    
def get_biggest_mission_id(dictionnary):
    """
    Utils function return the biggest mission_id from a list of missions in a dict.
    
    Args:
        dictionnary: the dict where are stored the missions.
    Returns:
        The biggest int.
    """
    higher_int = 0
    for key, value in dictionnary.items():
        if value['id'] > higher_int:
            higher_int = value['id']
    return higher_int

def compute_distance(coordinates_map):
    """
    Utils function to calculate the distance between each point from the drone map.
    
    Args:
        coordinates_map: the dict where all the coordinates / drone info are store.
    Returns:
        The distance in mm.
    """
    previous_point = [coordinates_map['x_init'],coordinates_map['y_init']]
    current_distance = 0
    for i in range(int((len(coordinates_map)-8)/2)):
        current_point = [coordinates_map[f'x_{i+1}'],coordinates_map[f'y_{i+1}']]
        distance = math.dist(previous_point, current_point)
        if distance > 10:
            current_distance += distance
        previous_point = current_point
    return math.floor(current_distance)

def compute_time_difference(start_date):
    """
    Utils function to compute time difference between now and a specified time.
    
    Args:
        start_date: datetime date format of the start of the mission.
    Returns:
        The time difference in seconds.
    """
    now = datetime.datetime.now()
    start_date = datetime.datetime.fromisoformat(str(start_date))
    time_difference = now - start_date
    return time_difference.seconds

