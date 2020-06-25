import psycopg2
from psycopg2 import OperationalError


### CHECK IF USER EXISTS ###
def user_exists(user_name):
    user_exist = execute_read_query(
        f"SELECT COUNT(*) FROM users WHERE username = \'{user_name}\'")
    exist_check = user_exist[0][0]
    return exist_check > 0


### SQL INIT ###
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(database="postgres", user="postgres",
                                      password="password", host="127.0.0.1",
                                      port="5432")
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


### SQL QUERY ###
def execute_query(query, arguments=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if arguments is None:
            cursor.execute(query)
        else:
            cursor.execute(query, arguments)
        connection.commit()
        print("Query executed successfully")
        return True
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return False

### GET TABLE VALUES ###
def execute_read_query(query, arguments=None):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        if arguments is None:
            cursor.execute(query)
        else:
            cursor.execute(query, arguments)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return False


# for debugging: export FLASK_ENV=development

# in flask_app directory:
# python3 -m venv venv
# source venv/bin/activate

# pip3 install flask
# pip3 install requests
# pip3 install psycopg2-binary

# to run:
# export FLASK_APP=server.py
# flask run

