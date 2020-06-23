from flask import Flask, render_template, request
from markupsafe import escape
import psycopg2
from psycopg2 import OperationalError

### BASIC INITIALIATION ###
app = Flask(__name__)

if __name__ == '__main__':
    app.run()


### SQL INIT ###
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(database="postgres", user="postgres",
                        password="password", host="127.0.0.1", port="5432")
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

### SQL QUERY ###
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

### GET TABLE VALUES ###
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return False


### GET, POST, AND DELETE ###
# get recieves data, post sends data
@app.route('/', methods=['GET', 'POST', 'DELETE'])
def user():
    con = create_connection()
    username = request.form['username']
    if request.method == 'POST':
        user_exist = execute_query(con, f"SELECT COUNT(*) WHERE username = {username}")
        max_id = execute_query(con, "SELECT MAX(id) FROM users")
        if user_exist > 0:
            return False
        else:
            idval = max_id + 1
            fistname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            addr = request.form['address']
            pswd = request.form['password']
            query = f"""INSERT INTO users (username, id, firstname, lastname,
            addr, pswd) VALUES ({username}, {idval}, {firstname},
            {lastname}, {email}, {addr}, {pswd})"""
            execute_query(con, query)
            return True

    else if request.method == 'GET':
        query = f"SELECT * FROM users WHERE username = {username}"
        resp = execute_read_query(con, query)
        if not resp:
            response = Response(response=json.dumps(resp), status=200, mimetype='application/json')
            return response
        else:
            response = Response(status=199)
            return response
        # 200 = standard ok status, 400 = user did not exist (client error)

    else if request.method == 'DELETE':
        query = "DELETE FROM users WHERE username = {username}"
        return execute_read_query(con, query)


### MODIFY USER ###
# The column name represents what user attribute to update
# ID val is accessible through user identifier method
@app.route('/partialmod/<col_name>', methods=['PUT'])
def update_user(col_name):
    idval = request.form['id']
    user_exist = execute_query(con, f"SELECT COUNT(*) WHERE id = {idval}")
    if user_exist > 0:
        return False
    else:
        replace = request.form[f'{col_name}']
        query = f"UPDATE users SET {col_name} = {replace} WHERE id = {idval}"
        execute_query(con, query)
        return True

### RECOVER ID ###
# Uses user email to recover user attributes. This can be used
# in tandem with the update_user method which takes a user id
@app.route('/identuser/', methods=['GET'])
def identify_user():
    email = request.form['email']
    resp = execute_read_query(con, "SELECT id FROM users WHERE email = {email}")
    if not resp:
        response = Response(response=json.dumps(resp), status=200, mimetype='application/json')
        return response
    else:
        response = Response(status=199)
        return response
        
# authentication: send username, we send hash method/salt back, front end hashes password
# and sends it back, we return password input == real password
# return creds




# for debugging: export FLASK_ENV=development

# in flask_app directory:
# python3 -m venv venv
# source venv/bin/activate

# to run:
# export FLASK_APP=server.py
# flask run

