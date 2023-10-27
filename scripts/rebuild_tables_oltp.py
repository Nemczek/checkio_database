from create_database import connect_to_database
import sqlite3 as sq
import json

def read_database_name_from_json(file):
    """
    Function reads database name from json file
    """

    with open(file, "r") as file:
        name_json = json.load(file)
    return name_json

def extract_task_to_table(cursor: sq.Cursor) -> None:
    """
    Function extracts task names from tasks table to match snowflake design in OLTP version of database
    """
    
    extrct_task_name_sql_string = """
    CREATE TABLE tasks_names (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    INSERT INTO tasks_names (name)
    SELECT DISTINCT task_name
    FROM entries;

    ALTER TABLE entries
    ADD COLUMN task_id INTEGER REFERENCES tasks (id) ON DELETE CASCADE;

    UPDATE entries
    SET task_id = (
        SELECT id
        FROM tasks_names
        WHERE name = task_name
    );

    ALTER TABLE entries
    DROP COLUMN task_name;
    """

    try:
        cursor.executescript(extrct_task_name_sql_string)
    except sq.Error as error:
        print(f'Failed during execution of extracting task to table script: {error}')

def extract_usernames_to_table(cursor: sq.Cursor) -> None: 
    """
    Function extracts usernames from username table to match snowflake design in OLTP version of database
    """
    extract_usernames_sql_string = """
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    INSERT INTO users (name)
    SELECT DISTINCT username
    FROM entries;

    ALTER TABLE entries
    ADD COLUMN user_id INTEGER REFERENCES users (id) ON DELETE CASCADE;

    UPDATE entries
    SET user_id = (
        SELECT id
        FROM users
        WHERE name = username
    );

    ALTER TABLE entries
    DROP COLUMN username;
    """

    try:
        cursor.executescript(extract_usernames_sql_string)
    except sq.Error as error:
        print(f'Failed during execution of username extracting script: {error}')

def extract_task_statuses_to_table(cursor: sq.Cursor):
    """
    Function extracts task statuses from tasks table to match snowflake design in OLTP version of database
    """
    
    extract_usernames_sql_string = """
    CREATE TABLE statuses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );

    INSERT INTO statuses (name)
    SELECT DISTINCT Task_status FROM entries;

    ALTER TABLE entries
    ADD COLUMN status_id INTEGER REFERENCES Task_status (id) ON DELETE CASCADE;

    UPDATE entries
        SET status_id = (
        SELECT id
        FROM statuses
        WHERE name = Task_status
    );

    ALTER TABLE entries
    DROP COLUMN Task_status;
    """

    try:
        cursor.executescript(extract_usernames_sql_string)
    except sq.Error as error:
        print(f'Failed during execution of statuses extracting script: {error}')

if __name__ == '__main__':
    db_name = read_database_name_from_json('test_database.json')
    connection = connect_to_database(db_name['name'])
    cursor = connection.cursor()

    extract_task_statuses_to_table(cursor)
    extract_usernames_to_table(cursor)
    extract_task_to_table(cursor)

    cursor.close()
    connection.close()

