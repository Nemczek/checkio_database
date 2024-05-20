import streamlit as st
import requests
import fetch_data
import get_slug
import sqlalchemy as db
import sqlite3 as sq
import pandas as pd
import create_database
import os
GROUP_PROGRESS_API_BASE = 'https://py.checkio.org/api/group-progress/'
BASE_URL = 'https://py.checkio.org/api/group-details/'
DB_NAME = 'test_database_OLTP'
DB_NAME2 = 'test_database_OLAP'
JSON_NAME = 'test_database'

st.markdown("<center><h1>pyCheckio database app</h1></center>", unsafe_allow_html=True)

# User checkio token
placeholder = st.empty()
token = st.text_input("Please paste your checkio token")

if token:
    base_with_token = BASE_URL + token
    all_classes_data = requests.get(base_with_token).json()['objects']

    classes = []
    class_slug = []
    for class_obj in all_classes_data:
        classes.append((class_obj["name"]))
    
    choosen_class = st.selectbox("Pick class to create database from", classes, index=None)
    
    for class_obj in all_classes_data:
        if class_obj["name"] == choosen_class:
            slug = class_obj["slug"]

    current_path = os.getcwd()
    save_path = current_path + r'\database'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    try:
        placeholder.text("Creating database")
        data_entries = fetch_data.fetch_entry_data(slug, token)
        data_tasks = fetch_data.fetch_task_data(slug, token)

        engine = create_database.create_sql_engine(DB_NAME)
        engine2 = create_database.create_sql_engine(DB_NAME2)

        # Creating tables in database. If table already exists, it appends new records.
        data_tasks.to_sql('tasks', con=engine, index=False, if_exists='append', schema=None)
        data_entries.to_sql('entries', con=engine, index=False, if_exists='append', schema=None)

        data_tasks.to_sql('tasks', con=engine2, index=False, if_exists='append', schema=None)
        data_entries.to_sql('entries', con=engine2, index=False, if_exists='append', schema=None)
        st.text("Done")
    except:
        pass








