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
        
        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode("utf-8")
        
        csv_tasks = convert_df(data_tasks)
        csv_entries = convert_df(data_entries)

        st.subheader("Preview of tasks data")
        with st.expander("Expand preview"):
            st.dataframe(data_tasks)
        st.download_button("Download tasks data as csv file", data=csv_tasks, file_name="tasks_data.csv")
        
        st.subheader("Preview of entries data")
        with st.expander("Expand preview"):
            st.dataframe(data_entries)
        st.download_button("Download entries data as csv file", data=csv_entries, file_name="entries_data.csv")

        # Plots and statistics for choosen student
        students = [student for student in data_entries["Username"].unique()]
        choosen_student = st.selectbox("Choose student to get details", students, index=None)

        database_subset = data_entries[data_entries["Username"] == choosen_student]
        st.subheader("Tasks done by student")
        st.dataframe(database_subset)

    except:
        pass









