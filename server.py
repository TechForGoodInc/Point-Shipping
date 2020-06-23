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

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
        return true
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return false

### GET TABLE ###
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
    

### GET AND POST ###
# get recieves data, post sends data
# delete, put (update/modify data?)
@app.route('/', methods=['GET', 'POST'])
def modifyuser():
    con = create_connection()
    if request.method == 'POST':
        username = request.form['username']
        user_exist = execute_query(con, f"SELECT COUNT(*) WHERE username = {username}")
        if user_exist > 0:
            return "Username taken"
        else:
            idval = request.form['id']
            fistname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            address = request.form['address']
            password = request.form['password']
            query = f"""INSERT INTO users VALUES ({username}, {idval}, {firstname},
            {lastname}, {email}, {address}, {password})"""
            execute_query(con, query)

    if request.method=='GET':
        username = request.form['username']
        query = f"SELECT * FROM users WHERE username = {username}"
        resp = execute_read_query(con, query)
        if not resp:
            response = Response(response=json.dumps(resp), status=200, mimetype='application/json')
            return response
        else:
            response=Response(status=199)
        # 200 = standard ok status, 199 = user did not exist
        
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
