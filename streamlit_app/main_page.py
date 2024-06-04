import streamlit as st
import requests
import fetch_data
import pandas as pd
import os
import numpy as np

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
    save_path = current_path + r'/database'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    try:
        if os.path.exists(fr"./database/task_data_{slug}.csv"):
            data_entries = pd.read_csv(fr"./database/entries_data_{slug}.csv")
            data_tasks = pd.read_csv(fr"./database/task_data_{slug}.csv")
        else:
            placeholder.text("Creating database")
            data_entries = fetch_data.fetch_entry_data(slug, token)
            data_tasks = fetch_data.fetch_task_data(slug, token)

            # "caching" database
            data_tasks.to_csv(fr"./database/task_data_{slug}.csv", index=False)
            data_entries.to_csv(fr"./database/entries_data_{slug}.csv", index=False)

        if st.button("Update database"):
            data_entries = fetch_data.fetch_entry_data(slug, token)
            data_tasks = fetch_data.fetch_task_data(slug, token)

        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode("utf-8")
        
        csv_tasks = convert_df(data_tasks)
        csv_entries = convert_df(data_entries)

        st.subheader("Preview of tasks data")
        with st.expander("Expand preview"):
            st.dataframe(data_tasks, hide_index=True)
        st.download_button("Download tasks data as csv file", data=csv_tasks, file_name="tasks_data.csv")
        
        st.subheader("Preview of entries data")
        with st.expander("Expand preview"):
            st.dataframe(data_entries, hide_index=True)
        st.download_button("Download entries data as csv file", data=csv_entries, file_name="entries_data.csv")

        # Plots and statistics for choosen student
        students = [student for student in data_entries["Username"].unique()]
        choosen_student = st.selectbox("Choose student to get details", students, index=None)

        if choosen_student:
            database_subset = data_entries[data_entries["Username"] == choosen_student]
            st.subheader(f"Tasks done by {choosen_student}")
            st.dataframe(database_subset, use_container_width=True, hide_index=True)
            
            st.subheader(f"Details of {choosen_student}")
            student_summary = pd.DataFrame([
                [database_subset["Votes"].replace("None", np.NaN).sum(),
                database_subset["Comments"].replace("None", np.NaN).sum(),
                database_subset[database_subset["Task_status"] == "published"].shape[0],
                database_subset[database_subset["Task_status"] == "opened"].shape[0],
                database_subset[database_subset["Task_status"] == "tried"].shape[0]]
            ], columns=["Received Votes", "Received Comments", "Published tasks", "Opened tasks", "Tried tasks"])
            st.dataframe(student_summary, hide_index=True)

            temp_df_votes = database_subset[["Task_name", "Votes"]].replace("None", 0)
            temp_df_comms = database_subset[["Task_name", "Comments"]].replace("None", 0)

            temp_df_votes = temp_df_votes[temp_df_votes["Votes"] != 0]
            temp_df_comms = temp_df_comms[temp_df_comms["Comments"] != 0]

            st.subheader("Number of votes for each task")
            st.bar_chart(temp_df_votes, x="Task_name", y="Votes")
            
            st.subheader("Number of comments for each task")
            st.bar_chart(temp_df_comms, x="Task_name", y="Comments")

            database_subset['Created_at'] = pd.to_datetime(database_subset['Created_at'])
            database_subset['Date'] = database_subset['Created_at'].dt.date
            task_counts = database_subset.groupby('Date').size().reset_index(name='Task_count')
            st.subheader("Number of tasks done")
            st.line_chart(task_counts, x="Date", y="Task_count", )
    # For debug change later
    except Exception as e:
        st.warning(e)









