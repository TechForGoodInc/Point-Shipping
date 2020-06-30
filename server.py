from flask import Flask, render_template, request, json
import requests
import interface as inter
import shipping as ez

### BASIC INITIALIATION ###
app = Flask(__name__)

if __name__ == '__main__':
    app.run()


### TESTS ###
@app.route('/database/')
def init():
    rqst = "SELECT * FROM users"
    resp = inter.execute_read_query(rqst)
    label_rqst = "SELECT * FROM labels"
    resp += inter.execute_read_query(label_rqst)
    to_send = app.response_class(response=json.dumps(resp), status=200,
                                 mimetype='application/json')
    return to_send


### GET, POST, AND DELETE ###
# get recieves data, post sends data
@app.route('/user/', methods=['GET', 'POST', 'DELETE'])
def user():
    user_name = request.form['username']

    if request.method == 'POST':
        if inter.user_exists(user_name):
            return app.response_class(status=409)
        # used to generate the user id (requires at least user
        # id to already exist)
        max_id = 0
        #max_id = inter.execute_query("SELECT MAX(id) FROM users")
        idval = max_id + 1
        email = request.form['email']
        sender_name = request.form['sender_name']
        sender_street = request.form['sender_street']
        sender_city = request.form['sender_city']
        sender_state = request.form['sender_state']
        sender_zip = request.form['sender_zip']
        sender_country = request.form['sender_country']
        ez_address_id = ez.get_address(sender_name, sender_street,
                                       sender_city, sender_state,
                                       sender_zip, sender_country)
        unencrypted_pw = request.form['password']
        encrypted = inter.encrypt_password(unencrypted_pw)
        # apostrophe escaped to work with SQL format
        query = f"""INSERT INTO users VALUES (\'{user_name}\', \'{idval}\',
            \'{email}\', \'{ez_address_id}\', \'{encrypted}\')"""
        if inter.execute_query(query):
            return app.response_class(status=200)
        else:
            return app.response_class(status=502)

    elif request.method == 'GET':
        query = f"SELECT * FROM users WHERE username = \'{user_name}\'"
        resp = inter.execute_read_query(query)
        if resp:
            response = app.response_class(response=json.dumps(resp),
                                          status=200,
                                          mimetype='application/json')
            return response
        else:
            return app.response_class(status=404)

    elif request.method == 'DELETE':
        if not inter.user_exists(user_name):
            return app.response_class(status=404)
        query = f"DELETE FROM users WHERE username = \'{user_name}\'"
        if inter.execute_query(query):
            return app.response_class(status=200)

    else:
        return app.response_class(status=400)


### MODIFY USER ###
# The column name represents what user attribute to update
# ID val is accessible through user identifier method
@app.route('/usermod/<col_name>/', methods=['PUT'])
def update_user(col_name):
    idval = request.form['id']
    if inter.user_exists(idval, 'id'):
        replace = request.form[f"{col_name}"]
        query = f"UPDATE users SET {col_name} = \'{replace}\' WHERE id = \'{idval}\'"
        if inter.execute_query(query):
            return app.response_class(status=200)

    return app.response_class(status=404)


### RECOVER ID ###
# Uses user email to recover user attributes. This can be used
# in tandem with the update_user method which takes a user id
@app.route('/identuser/', methods=['GET'])
def identify_user():
    email = request.form['email']
    if inter.user_exist(email, "email"):
        resp = inter.execute_read_query(
            f"SELECT id FROM users WHERE email = \'{email}\'")
        response = app.response_class(response=json.dumps(resp[0][0]),
                                      status=200,
                                      mimetype='applications/json')
        return response
    else:
        return app.response_class(status=404)


@app.route('/validate/', methods=['GET'])
def validate():
    userid = request.form['userid']
    input_pw = request.form['password']
    if inter.password_match(userid, input_pw):
        return app.response_class(status=200)
    else:
        return app.response_class(status=406)


### ADDS PACKAGE ###
# requires full package information to create package object
# through ezpost
@app.route('/addpackage/', methods=['POST'])
def addpackage():

    userid = request.form['userid']

    dest_name = request.form['dest_name']
    dest_street = request.form['dest_street']
    dest_city = request.form['dest_city']
    dest_state = request.form['dest_state']
    dest_zip = request.form['dest_zip']
    dest_country = request.form['dest_country']
    to_address = ez.get_address(dest_name, dest_street, dest_city,
                                dest_state, dest_zip, dest_country)

    query = f"SELECT ez_address_id FROM users WHERE id = \'{userid}\'"
    user_addr = inter.execute_read_query(query)

    i_length = request.form['length']
    i_width = request.form['width']
    i_height = request.form['height']
    i_weight = request.form['weight']
    parcel = ez.create_parcel(i_length, i_width, i_height, i_weight)

    shipment = ez.create_shipment(parcel, to_address, user_addr)
    add_query = f"INSERT INTO labels (userid, shipment) VALUES (\'{userid}\', \'{shipment}\')"

    return app.response_class(status=200)


@app.route('/previouspackages/<userval>/', methods=['GET'])
def get_packages(userval):
    query = f"SELECT * FROM labels WHERE userid = \'{userval}\'"
    resp = inter.execute_read_query(query)
    response = app.response_class(response=json.dumps(resp), status=200,
                                  mimetype='application/json')
    return response

# user checked out and paid for package
# send post request with new shipping label info and username
# return "ok"

# requests.post

