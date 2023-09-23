import requests
import pandas as pd
from collections import Counter

# Base API url
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


def fetch_entry_data(slug: str, token: str) -> pd.DataFrame:
    """
    Function returnes data about all tasks solved by students from given class
    """
    progress_url_with_slug = f"{GROUP_PROGRESS_API_BASE}{token}&slug={slug}"
    progress_data = requests.get(progress_url_with_slug).json()['objects']

    # Extract data about tasks to list of lists
    list_of_entries = []

    for task in progress_data:
        task_name = task['title']

        for entry in task['data']:
            username = entry['username']
            status = entry['status']

            if len(entry['solutions']) == 0:
                url, createdAt, votes, comments = "None", "None", "None", "None"
            else:
            # I'm taking only first solution / add all solutions later 
            # just another for loop
                url = entry['solutions'][0]['url']
                createdAt = entry['solutions'][0]['createdAt']
                votes = entry['solutions'][0]['votes']
                comments = entry['solutions'][0]['comments']

            list_of_entries.append([username, status, task_name, createdAt, votes, comments, url])

    # Convert list of lists to pandas data frame
    entry_data = pd.DataFrame(list_of_entries, columns=['Task', 'Votes', 'Comments',
                                                    'Opened', 'Published', 'Tried',
                                                    'New'])
    