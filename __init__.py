from flask import Flask, render_template, request, json
from flask_cors import CORS
import requests
from modules import interface as inter
from modules import shipping as ship
from modules import payment as pay

### BASIC INITIALIATION ###
app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# userid is the same as the package deliver number
@app.route('/getpackages/<userid>/', methods=['GET'])
def packages(userid):
    resp = ship.get_shipments(userid)
    print(resp)
    if resp:
        return app.response_class(status=200)
    else:
        return app.response_class(status=400)


### POST AND DELETE ###
# post creates a new user, delete deletes a user
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
        if inter.execute_query(query) and pay.new_user(idval, email):
            return app.response_class(status=200)

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
        print(query)
        if inter.execute_query(query):
            query = f"SELECT * FROM users WHERE id = \'{idval}\'"
            resp = inter.execute_read_query(query)
            if resp:
                key_list = ["username", "id", "email", "sender", "street",
                            "city", "state", "zip", "country", "password"]
                full_resp = dict(zip(key_list, resp[0]))
                stripe_id = pay.get_customer_id(full_resp["id"])
                full_resp["stripe_id"] = stripe_id
                payment_options = pay.get_payment_options(
                    full_resp["stripe_id"])
                full_resp["payment_options"] = payment_options
                print(full_resp)
                response = app.response_class(response=json.dumps(full_resp),
                                              status=200,
                                              mimetype='application/json')
                return response
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
                                      mimetype='application/json')
        return response
    else:
        return app.response_class(status=404)


### CONFIRM PASSWORD ###
# If passwords match, user credentials are returned. Otherwise,
# an error is returned.
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
            stripe_id = pay.get_customer_id(full_resp["id"])
            full_resp["stripe_id"] = stripe_id
            payment_options = pay.get_payment_options(full_resp["stripe_id"])
            full_resp["payment_options"] = payment_options
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
def getrates():
    if request.method == 'POST':
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
                                request.form['width'], request.form['length'],
                                request.form['category'],
                                request.form['currency'],
                                request.form['customs_val'])
        try:
            rates = resp['rates']
            return app.response_class(status=201, response=json.dumps(resp),
                                      mimetype='application/json')
        except KeyError:
            return app.response_class(status=200, response=json.dumps(resp),
                                      mimetype='application/json')


### ADDS PACKAGE ###
# requires full package information to create package object
# through easyship
@app.route('/addpackage/', methods=['POST'])
def addpackage():
    user_id = request.form['user_id']
    courier_id = request.form['courier_id']
    resp = ship.create_shipment(user_id, courier_id,
                                request.form['platform_name'],
                                request.form['platform_order_number'],
                                request.form['dest_name'],
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
        print(resp)
        success_check = inter.record_package(user_id, resp[0], resp[1])
        print(success_check)
        # resp[0] = courierid, resp[1] = shipmentid
        label_resp = ship.buy_labels(resp)
        return app.response_class(status=200, response=json.dumps(label_resp))


@app.route('/deletepackage/', methods=['DELETE'])
def deletepackage():
    shipid = request.form['shipmentid']
    check = ship.delete_package(shipid)
    print(check.status_code)
    return app.response_class(status=check.status_code,
                              response=json.dumps(check))


@app.route('/cardoptions/', methods=['POST'])
def card_options():
    userid = request.form["userid"]
    sources = pay.get_card_options(userid)
    return app.response_class(status=200, response=json.dumps(sources),
                              mimetype='application/json')


@app.route('/addpayment/', methods=['POST'])
def create_payment():
    if request.method == 'POST':
        print("beepboop")
        stripeid = request.form["stripeid"]
        card_num = request.form["card_num"]
        exp_month = request.form["exp_month"]
        exp_year = request.form["exp_year"]
        cvc = request.form["cvc"]
        resp = pay.add_payment_method(
            stripeid, card_num, exp_month, exp_year, cvc)
        return app.response_class(status=200, response=json.dumps(resp),
                                  mimetype='application/json')


@app.route('/chargecard/', methods=['POST'])
def charge_card():
    if request.method == 'POST':
        amount = request.form["amount"]
        resp = pay.charge_card(amount)
        return app.response_class(status=200, response=json.dumps(resp),
                                  mimetype='application/json')

# return payment method
# create/charge card
# sudo service apache2 restart
# cat /var/log/apache2/error.log
