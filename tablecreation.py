import psycopg2
from psycopg2 import OperationalError


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(database="postgres", user="postgres",
                        password="password", host="127.0.0.1", port="5432")
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
        return True
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return False

create_users_table = """ 
CREATE TABLE IF NOT EXISTS users (
  username TEXT NOT NULL,
  id INTEGER,
  firstname TEXT NOT NULL, 
  lastname TEXT NOT NULL,
  address VARCHAR,
  password VARCHAR,
  previous_labels INTEGER
)
"""

create_label_table = """
CREATE TABLE IF NOT EXISTS labels (
    user_id INTEGER,
    destination_address VARCHAR,
    sender_address VARCHAR,
    data DATE,
    price FLOAT,
    carrier VARCHAR
)
"""

con = create_connection()
print(execute_query(con, create_users_table))
print(execute_query(con, create_label_table))