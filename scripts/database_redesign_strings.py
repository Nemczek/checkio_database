# SQL code used to extract usernames to new table
username_table_sql_string = """
CREATE TABLE users(
  	id INTEGER PRIMARY KEY AUTOINCREMENT,
  	name TEXT NOT NULL
);

INSERT INTO users (name)
SELECT DISTINCT username
FROM entry_df;

ALTER TABLE entry_df
ADD COLUMN user_id INTEGER REFERENCES users (id) ON DELETE CASCADE;

UPDATE entry_df
SET user_id = (
  SELECT id
  FROM users
  WHERE name = username
);

ALTER TABLE entry_df
DROP COLUMN username;
"""

# SQL code used to extract task names to new table
task_table_sql_string = """
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

INSERT INTO tasks (name)
SELECT DISTINCT task_name
FROM entry_df;

ALTER TABLE entry_df
ADD COLUMN task_id INTEGER REFERENCES tasks (id) ON DELETE CASCADE;

UPDATE entry_df
SET task_id = (
  SELECT id
  FROM tasks
  WHERE name = task_name
);

ALTER TABLE entry_df
DROP COLUMN task_name;
"""

# SQL code to extract statuses to new table
status_table_sql_string = """
CREATE TABLE statuses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT
);

INSERT INTO statuses (name)
SELECT DISTINCT status FROM entry_df;

ALTER TABLE entry_df
ADD COLUMN status_id INTEGER REFERENCES statuses (id) ON DELETE CASCADE;

UPDATE entry_df
SET status_id = (
  SELECT id
  FROM statuses
  WHERE name = status
);

ALTER TABLE entry_df
DROP COLUMN status;
"""

