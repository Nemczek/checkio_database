import requests

GROUP_PROGRESS_API_BASE = 'https://py.checkio.org/api/group-progress/'
BASE_URL = 'https://py.checkio.org/api/group-details/'

def get_token(path: str) -> str:
    """
    Function gets file path, and returns base API url with group token given by Pycheckio platform
    """

    try:
        with open(path, 'r') as file:
            token = file.readline()
            return token
        
    except FileNotFoundError:
        print(f'{path} does not exisits. You need to provide a file with token from pycheckio site.')
        # In future add entry to the log file

def get_class_slug(token: str) -> str:
    """
    Function returns slug parameter needed by API to retrive data about choosen class
    """
    base_with_token = BASE_URL + token
    all_classes_data = requests.get(base_with_token).json()['objects']

    # Loop for asking user to provide correct name of class
    while True:
        print('These are all classes assigned to a user. Type name of a class you want to make a database for')
        for class_obj in all_classes_data:
            print(class_obj['name'])
        
        name = input('>>>')

        for class_obj in all_classes_data:
            if class_obj['name'] == name:
                return class_obj['slug']
        print('You provided wrong name. Please try again.')