import psycopg2
from psycopg2 import OperationalError
import bcrypt
import json


### SQL INIT ###
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(database="postgres", user="postgres",
                                      host="127.0.0.1",
                                      port="5432")
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


### SQL QUERY ###
def execute_query(query, arguments=None):
    connection = create_connection()
    with connection:
        try:
            cursor = connection.cursor()
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
    result = None
    with connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return False


### CHECK IF USER ASPECT EXISTS ###
def user_exists(userval, column_name="username"):
    user_exist = execute_read_query(
        f"SELECT COUNT(*) FROM users WHERE {column_name} = \'{userval}\'")
    exist_check = user_exist[0][0]
    return exist_check > 0


### CHECK IF USERNAME IS TAKEN ###
def username_exists(username):
    check = execute_read_query(
        f"SELECT COUNT(*) FROM users WHERE \"username\" = \'{username}\'")
    exist_check = check[0][0]
    if exist_check > 0:
        return "True"
    else:
        return "False"


### CHECK IF PASSWORDS MATCH ###
# userpassword = b'text'
def password_match(username, input_password):
    query = f"SELECT password FROM users WHERE username = \'{username}\'"
    current_password = execute_read_query(query)
    correct = current_password[0][0].encode("utf-8")
    input_pw = input_password.encode("utf-8")
    return bcrypt.checkpw(input_pw, correct)


### ENCRYPT PASSWORD ###
def encrypt_password(password_input):
    byt_pswd = password_input.encode('utf-8')
    hashed = bcrypt.hashpw(byt_pswd, bcrypt.gensalt())
    hash_test = hashed.decode("utf-8")
    return hashed.decode("utf-8")


def record_package(userid, courierid, shipmentid):
    query = f"""INSERT INTO labels VALUES (\'{userid}\', \'{courierid}\',
                \'{shipmentid}\')"""
    success_check = execute_query(query)
    return success_check


def update_code(code, userid):
    query = f"""UPDATE users SET recoveryid = \'{code}\'
                WHERE id = \'{userid}\'"""
    success_check = execute_query(query)
    return success_check


def code_check(code, userid):
    query = f"""SELECT * FROM users WHERE \'id\' = \'{userid}\'
                AND \'recoveryid\' = \'{code}\'"""
    check = execute_read_query(query)
    try:
        return check[0][0] > 0
    except IndexError:
        return False

# for debugging: export FLASK_ENV=development

# to run:
# export FLASK_APP=server.py
# flask run

# AzureUser@52.188.71.21
# Pointshipping12
# sudo ssh -i /Users/emilylouden/Desktop/key.ppk AzureUser@52.188.13.210
