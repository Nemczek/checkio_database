import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
import sqlite3 as sq
import pandas as pd
import fetch_data
import get_slug
import os

def create_sql_engine(name_of_database_file: str) -> db.engine.base.Engine:
    """
    Function creates our database file and returnes engine to database *.db extension is added automatically
    """
    
    engine = db.create_engine(f'sqlite:///{name_of_database_file}.db')

    return engine

def connect_to_database(db_name: str) -> sq.Connection:
    """
    Function returns connetion object to our database. *.db extension is added automatically
    """
    
    try:
        connection = sq.connect(f'{db_name}.db')
        return connection
    
    except sq.Error as error:
        print(f'Failed to connect to database {error}') # Add log entry later 

if __name__ == '__main__':
    token = get_slug.get_token('checkio_token.txt')
    slug = get_slug.get_class_slug(token)

    data_tasks = fetch_data.fetch_task_data(slug, token)
    data_entries = fetch_data.fetch_entry_data(slug, token)

    engine = create_sql_engine('test_database')

    # Creating tables in database. If table already exists, it appends new records.
    data_tasks.to_sql('tasks', con=engine, index=False, if_exists='append', schema=None)
    data_entries.to_sql('entries', con=engine, index=False, if_exists='append', schema=None)

    # Simple testing
    connection = connect_to_database('test_database')
    cursor = connection.cursor()

    query = "SELECT * FROM tasks"
    result = cursor.execute(query)
    rows = result.fetchall()

    print(pd.DataFrame(rows, columns=map(lambda x: x[0], result.description)))

    query2 = "SELECT * FROM entries"
    result2 = cursor.execute(query2)
    rows2 = result.fetchall()

    print(pd.DataFrame(rows2, columns=map(lambda x2: x2[0], result2.description)))

    





