import sqlalchemy as db
from sqlalchemy_utils import database_exists, create_database
import sqlite3 as sq

def create_sql_engine(name: str) -> db.engine.base.Engine:
    """
    Function creates our database file and returnes engine
    """
    
    engine = db.create_engine(f'sqlite:///{name}')

    # Code below creates database file if it's not exists
    if not database_exists(engine.url):
        create_database(engine.url)

    return engine

def connect_to_database(engine: db.engine.base.Engine) -> sq.Connection:
    """
    Function returns connetion object to our database
    """
    
    try:
        connection = sq.connect(engine)
        return connection
    
    except sq.Error as error:
        print(f'Failed to connect to database {error}') # Add log entry later 