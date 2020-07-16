from flask import Flask, render_template, request, json
from flask_cors import CORS
import requests
import interface as inter
import shipping as ship

### BASIC INITIALIATION ###
app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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
@app.route('/user/', methods=['POST', 'DELETE'])
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
        unencrypted_pw = request.form['password']
        encrypted = inter.encrypt_password(unencrypted_pw)
        quer1 = f"INSERT INTO users VALUES (\'{user_name}\', \'{idval}\',"
        quer2 = f"\'{email}\', \'{sender_name}\', \'{sender_street}\',"
        quer3 = f"\'{sender_city}\', \'{sender_state}\', \'{sender_zip}\',"
        quer4 = f"\'{sender_country}\', \'{encrypted}\')"
        query = " ".join([quer1, quer2, quer3, quer4])
        if inter.execute_query(query):
            return app.response_class(status=201)
        else:
            return app.response_class(status=502)

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
@app.route('/identuser/<email>', methods=['GET'])
def identify_user(email):
    if inter.user_exists(email, "email"):
        resp = inter.execute_read_query(
            f"SELECT id FROM users WHERE email = \'{email}\'")
        response = app.response_class(response=json.dumps(resp[0][0]),
                                      status=200,
                                      mimetype='applications/json')
        return response
    else:
        return app.response_class(status=404)


@app.route('/validate/', methods=['POST'])
def validate():
    username = request.form['username']
    input_pw = request.form['password']
    if inter.password_match(username, input_pw):
        query = f"SELECT * FROM users WHERE username = \'{username}\'"
        resp = inter.execute_read_query(query)
        print(resp)
        if resp:
            response = app.response_class(response=json.dumps(resp),
                                          status=200,
                                          mimetype='application/json')
            return response
        else:
            return app.response_class(status=404)
    else:
        return app.response_class(status=406)


### SELECT RATE FOR PACKAGE ###
# returns courier id
@app.route('/getrates/', methods=['POST'])
def getrate():
    resp = ship.select_rate(request.form['origin_city'],
                            request.form['origin_state'],
                            request.form['origin_country'],
                            request.form['origin_zip'],
                            request.form['dest_city'],
                            request.form['dest_state'],
                            request.form['dest_country'],
                            request.form['dest_zip'],
                            request.form['tax_payer'],
                            request.form['insured'],
                            request.form['weight'], request.form['height'],
                            request.form['width'], request.form['width'],
                            request.form['category'],
                            request.form['currency'],
                            request.form['customs_val'])
    rate_dict = json.loads(resp.decode('utf8'))
    return app.response_class(status=200, response=rate_dict)


### ADDS PACKAGE ###
# requires full package information to create package object
# through easyship
@app.route('/addpackage/', methods=['POST'])
def addpackage():
    user_id = request.form['user_id']
    courier_id = request.form['courier_id']
    resp = ship.create_shipment(user_id, courier_id, request.form['dest_name'],
                                request.form['dest_add1'],
                                request.form['dest_add2'],
                                request.form['dest_city'],
                                request.form['dest_state'],
                                request.form['dest_zip'],
                                request.form['dest_country'],
                                request.form['dest_phone'],
                                request.form['item_description'],
                                request.form['weight'], request.form['height'],
                                request.form['width'], request.form['length'],
                                request.form['category'],
                                request.form['currency'],
                                request.form['customs_val'],
                                request.form['dest_email'])
    decoded = json.loads(resp.decode('utf8'))
    shipment_dict = decoded['shipment']
    courier_id = shipment_dict['selected_courier']['id']
    shipment_id = shipment_dict['easyship_shipment_id']
    label_resp = ship.buy_labels(courier_id, shipment_id)
    return app.response_class(status=200, response=label_resp)


# user checked out and paid for package
# send post request with new shipping label info and username
# return "ok"
