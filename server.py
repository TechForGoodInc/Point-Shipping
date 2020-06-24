from flask import Flask, render_template, request, json
from markupsafe import escape
import requests
import psycopg2
from psycopg2 import OperationalError

### BASIC INITIALIATION ###
app = Flask(__name__)

if __name__ == '__main__':
   app.run()

### TESTS ###
@app.route('/')
def init():
    con = create_connection()
    request = "SELECT * FROM users"
    resp = execute_read_query(con, request)
    to_send = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
    return to_send

@app.route('/test/<col_type>')
def test(col_type):
    con = create_connection()
    query = f"SELECT {col_type} from users"
    resp = execute_read_query(con, query)
    to_send = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
    return to_send

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
            email, addr, pswd) VALUES ({username}, {idval}, {firstname},
            {lastname}, {email}, {addr}, {pswd})"""
            execute_query(con, query)
            return True

    elif request.method == 'GET':
        query = f"SELECT * FROM users WHERE username = {username}"
        resp = execute_read_query(con, query)
        if not resp:
            response = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
            return response
        else:
            response = app.response_class(status=400)
            return response
        # 200 = standard ok status, 400 = user did not exist (client error)

    elif request.method == 'DELETE':
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
        response = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
        return response
    else:
        response = app.response_class(status=199)
        return response

@app.route('/validate/', methods=['POST'])
def validate():
    username = request.form['username']
    query = f"SELECT pswd FROM users WHERE username = {username}"
    con = create_connection()
    resp = execute_read_query(con, query)
    if not resp:
        response = app.response_class(response=json.dumps(resp), status = 200, mimetype='application/json')
        return response
    else:
        return False

@app.route('/authorize/', methods=['GET'])
def postingAndVerifyingPwrd():
    if verifyPasswrd:
        if request.method == 'POST':
            username = request.form['username']
            query = f"SELECT pswd FROM users WHERE username = {username}"
            con = create_connection()
            resp = execute_read_query(con, query)
            if not response:
                return "user does not exist"
            else:
                if request.form['password'] == resp:
                    return "pw verified"
                else:
                    return "incorrect pw"

@app.route('/addpackage/<username>/', methods=['POST'])
def addpackage(username):
    con = create_connection()
    userid = request.form['userid']
    destination_address = request.form['destination_address']
    sender_address = request.form['sender_address']
    send_date = request.form['send_date']
    price = request.form['price']
    carrier = request.form['carrier']
    date = request.form['date']
    query = f"""INSERT INTO labels (userid, destination_address, sender_address,
    send_date, price, carrier) VALUES ({userid}, {destination_address}, {sender_address},
    {send_date}, {price}, {carrier}, {date})"""
    return execute_query(con, query)

@app.route('previouspackages/<userval>/', methods=['GET'])
def get_packages(userval):
    con = create_connection()
    query = f"SELECT * FROM labels WHERE userid = {userval}"
    return execute_query(con, query)

# user checked out and paid for package
# send post request with new shipping label info and username
# return "ok"

# for tomorrow:
# create a user (username, password, email, etc.)
# get username and password --- Chris

# package labels, addresses, connect to user (user id same as package table?)

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

