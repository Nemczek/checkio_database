import requests
import pandas as pd
from collections import Counter

# Base API url
GROUP_PROGRESS_API_BASE = 'https://py.checkio.org/api/group-progress/'
BASE_URL = 'https://py.checkio.org/api/group-details/'

def fetch_task_data(slug: str, token: str) -> pd.DataFrame:
    """
    Function returnes data about all tasks solved by students from given class
    """
    progress_url_with_slug = f"{GROUP_PROGRESS_API_BASE}{token}&slug={slug}"
    progress_data = requests.get(progress_url_with_slug).json()['objects']

    # Extract data about tasks to list of lists
    list_of_tasks = []
    for task in progress_data:
        num_of_votes = 0
        num_of_comments = 0
        list_of_statuses = []

        for entry in task['data']:
            list_of_statuses.append(entry['status'])

            for solution in entry['solutions']:
                num_of_votes += solution['votes']
                num_of_comments += solution['comments']

        counter_object = Counter(list_of_statuses)
        list_of_tasks.append([task['title'], num_of_votes, num_of_comments,
                                counter_object['opened'], counter_object['published'],
                                counter_object['tried'], counter_object['new']])

    # Convert list of lists to pandas data frame
    task_data = pd.DataFrame(list_of_tasks, columns=['Task', 'Votes', 'Comments',
                                                    'Opened', 'Published', 'Tried',
                                                    'New'])
    return task_data

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
    entry_data = pd.DataFrame(list_of_entries, columns=['Username', 'Task_status', 'Task_name',
                                                    'Created_at', 'Votes', 'Comments',
                                                    'Solution_url'])
    return entry_data