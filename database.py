import firebase_admin, datetime, json
from firebase_admin import credentials, db
from utils import get_biggest_mission_id

DB_URL = ''

def init_db(path_to_credentials = ''):
    """Initialize the database.
    """
    cred = credentials.Certificate(path_to_credentials)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DB_URL
        })

def db_get_mission(mission_id, search_key = ''):
    """ Get mission data in Firebase RTDB.

    Args:
        mission_id: The mission Id that you would like to get data from.
        search_key: (Optional) the exact key that you are looking for. (default return everything)

    Returns: 
        The requested data.
    """
    if search_key == '':
        ref = db.reference(f'/Mission_list/{mission_id}')
    else:
        ref = db.reference(f'/Mission_list/{mission_id}/{search_key}')
    
    try:
        return ref.get()
    except:
        return None

def db_push_new_mission(drone_amount, env='Réel'):
    """ Push a new mission in Firebase RTDB.

    Args:
        drone_amount: Amount of drones in the mission.
        env: (Optional) The environement Réel (default) or Simulation.

    Returns: 
        The new mission id.
    """
    ref = db.reference('/Mission_list')
    data = ref.get()
    new_mission_id = get_biggest_mission_id(data)+1
    drone_init_data = {}
    for i in range(drone_amount):
        drone_init_data[f'drone_{i+1}'] = {"speed": -1,"battery": -1, "status":"Chargement", "total_distance": 0, "x_init" :0.0000, "y_init" :0.0000, "x_current" : 0.0, "y_current" :0.0}
        sensors = {}
        sensors['data_init'] = {"x" :0.0000, "y" :0.0000}
        drone_init_data[f'drone_{i+1}_sensors'] = sensors
    new_mission = {
        "date" : str(datetime.datetime.now()),
        "id" : new_mission_id,
        "state": "En cours",
        "drone_amount" : drone_amount,
        "environment" : env,
        "map": drone_init_data,
        "fly_time": 0,
    }
    pushed_response = ref.push(new_mission)
    return new_mission_id, drone_init_data, pushed_response.key

def db_update_mission(mission_id, new_mission_json):
    """ Update mission data in Firebase RTDB.

    Args:
        mission_id: The id of the mission you want to update.
        new_mission_json: The new mission dict.
    """

    ref = db.reference(f'/Mission_list/{mission_id}/')
    ref.update(new_mission_json)

def db_new_log_entry(string_to_push, mission_id = -1):
    """Add a new log entry to the DB.

    Args:
        string (string): string to push to the DB based on date.
        mission_id (int, optional): Mission id to link the log to. Defaults to -1.
    """
    ref = db.reference('/Log_Files/')
    today = datetime.datetime.today()
    date_formatted = datetime.datetime.date(today)
    hours_formatted = datetime.datetime.time(today).replace(microsecond=0)
    log_entry_json = {}
    log_entry_json[f'{mission_id}/{date_formatted}/{hours_formatted}'] = string_to_push
    ref.update(log_entry_json)

def db_get_log_file(**kwargs):
    """Call log file DB to get data. Use mission arg to get specific missions logs. Use date arg to get specific mission date. Leave empty for default logs.

    Returns:
        json: Can be none if empty or a json of the returned logs.
    """
    ref = db.reference('/Log_Files/')
    full_list = ref.get()
    mission_id = -1
    date_formated = '1999-01-01'
    for key, value in kwargs.items():
        if key == 'mission':
            mission_id = value
        elif key == 'date':
            date_formated = datetime.datetime.date(value)
        else:
            return None
    if date_formated == '1999-01-01':
        return full_list[f'{mission_id}']
    return full_list[f'{mission_id}'][f'{date_formated}']