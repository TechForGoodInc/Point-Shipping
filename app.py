from flask import Flask, render_template, request, json
from flask_cors import CORS
import requests
from modules import interface as inter
from modules import shipping as ship
import stripe

stripe.api_key = "sk_test_51H60XYAzJnRyZcvUC1Fanr3dfwLFo6XR1Ne1wq231HFeev2813AaQZXHQQWSrv2NT3jnwUqrqDapYvivHoMr051l00tz2S4nM2"


### BASIC INITIALIATION ###
app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/packages/<userid>/', methods=['GET'])
def packages(userid):
    label_rqst = f"SELECT * FROM labels WHERE userid = \'{userid}\'"
    resp = inter.execute_read_query(label_rqst)
    labels = ["userid", "platform", "dest_name", "dest_add1", "dest_add2",
              "dest_city", "dest_state", "dest_zip", "dest_country",
              "dest_number", "dest_email", "pkg_length", "pkg_width",
              "pkg_height", "pkg_weight", "courierid"]
    final_resp = []
    for package in resp:
        final_resp.append(dict(zip(labels, package)))
    to_send = app.response_class(response=json.dumps(final_resp), status=200,
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
@app.route('/identuser/', methods=['POST'])
def identify_user():
    email = request.form['email']
    if inter.user_exists(email, "email"):
        resp = inter.execute_read_query(
            f"SELECT * FROM users WHERE email = \'{email}\'")
        key_list = ["username", "id", "email", "sender", "street",
                    "city", "state", "zip", "country", "password"]
        full_resp = dict(zip(key_list, resp[0]))
        response = app.response_class(response=json.dumps(full_resp),
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
        if resp:
            key_list = ["username", "id", "email", "sender", "street",
                        "city", "state", "zip", "country", "password"]
            full_resp = dict(zip(key_list, resp[0]))
            response = app.response_class(response=json.dumps(full_resp),
                                          status=200,
                                          mimetype='application/json')
            return response
        else:
            return app.response_class(status=404)
    else:
        return app.response_class(status=406)


### SELECT RATE FOR PACKAGE ###
# returns list of possible rates given the package/origin/destination
# aspects
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
    if len(resp['rates']) == 0:
        return app.response_class(status=500, response=json.dumps(resp))
    return app.response_class(status=200, response=json.dumps(resp))


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
    if type(resp) is not list:
        return app.response_class(status=500, response=json.dumps(resp))
    else:
        success_check = inter.record_package(user_id, resp[0], resp[1])
        label_resp = ship.buy_labels(resp[1:])
        return app.response_class(status=200, response=json.dumps(label_resp))


@app.route('/payment/', methods=['POST'])
def create_payment():
    try:
        order_amount = request.form['cost']
        intent = stripe.PaymentIntent.create(
            amount=order_amount,
            currency='usd'
        )
        resp = dict(intent)
        return app.response_class(status=200, response=json.dumps(resp))
    except Exception as e:
        resp = str(e)
        return app.response_class(status=403, response=json.dumps(resp))
