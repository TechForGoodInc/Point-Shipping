from flask import Flask, render_template, request, json
from flask_cors import CORS
import requests
from random import randint
from modules import interface as inter
from modules import shipping as ship
from modules import payment as pay
from modules import send_email as mail


### BASIC INITIALIATION ###
app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/getdatabase/', methods=['GET'])
def getdatabase():
    query = "SELECT * FROM users"
    resp = inter.execute_read_query(query)
    print(resp)
    return app.response_class(status=200, response=json.dumps(resp),
                              mimetype='application/json')


@app.route('/getpackages/<userid>/', methods=['GET'])
def packages(userid):
    resp = ship.get_package(userid)
    resp_dict = {'packages': resp}
    print(type(resp_dict))
    print(resp_dict)
    if resp:
        return app.response_class(status=200, response=json.dumps(resp_dict),
                                  mimetype='application/json')
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
        max_id = inter.execute_read_query("SELECT COUNT(*) FROM users")
        idval = max_id[0][0] + 1
        email = request.form['email']
        sender_name = request.form['sender_name']
        sender_street = request.form['sender_street']
        sender_city = request.form['sender_city']
        sender_state = request.form['sender_state']
        sender_zip = request.form['sender_zip']
        sender_country = request.form['sender_country']
        unencrypted_pw = request.form['password']
        encrypted = inter.encrypt_password(unencrypted_pw)
        quer1 = f"INSERT INTO users VALUES (\'{user_name}\', \'{idval}\', \'000000\', "
        quer2 = f"\'{email}\', \'{sender_name}\', \'{sender_street}\',"
        quer3 = f"\'{sender_city}\', \'{sender_state}\', \'{sender_zip}\',"
        quer4 = f"\'{sender_country}\', \'{encrypted}\')"
        query = " ".join([quer1, quer2, quer3, quer4])
        if inter.execute_query(query) and pay.new_user(idval, email):
            print("user added")
            return app.response_class(status=200)

    elif request.method == 'DELETE':
        if not inter.user_exists(user_name):
            return app.response_class(status=404)
        query = f"DELETE FROM users WHERE username = \'{user_name}\'"
        if inter.execute_query(query):
            return app.response_class(status=200)

    else:
        return app.response_class(status=400)


### CHECK IF USERNAME IS ALREADY IN USE ###


@app.route('/userexists/', methods=['GET'])
def user_exists():
    if request.method == 'GET':
        username = request.form["username"]
        check = inter.username_exists(username)
    return app.response_class(status=200, response=json.dumps(check),
                              mimetime='application/json')


### MODIFY USER ###
# The column name represents what user attribute to update
# ID val is accessible through user identifier method
@app.route('/usermod/<col_name>/', methods=['PUT'])
def update_user(col_name):
    idval = request.form['id']
    if inter.user_exists(idval, 'id'):
        replace = request.form[f"{col_name}"]
        if col_name == "password":
            replace = inter.encrypt_password(replace)
        query = f"UPDATE users SET {col_name} = \'{replace}\' WHERE id = \'{idval}\'"
        print(query)
        if inter.execute_query(query):
            query = f"SELECT * FROM users WHERE id = \'{idval}\'"
            resp = inter.execute_read_query(query)
            if resp:
                key_list = ["username", "id", "recovery_key", "email",
                            "sender", "street", "city", "state", "zip",
                            "country", "password"]
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
    print("here!!!\n\n\n")
    email = request.form['email']
    username = request.form['username']
    if inter.user_exists(email, "email"):
        resp = inter.execute_read_query(
            f"SELECT * FROM users WHERE email = \'{email}\'")
        key_list = ["username", "id", "recoverid", "email", "sender", "street",
                    "city", "state", "zip", "country", "password"]
        full_resp = dict(zip(key_list, resp[0]))
        if username == full_resp["username"]:
            response = app.response_class(response=json.dumps(full_resp),
                                          status=200,
                                          mimetype='application/json')
            return response
        else:
            return app.response_class(status=409)
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
            key_list = ["username", "id", "recovery_id", "email", "sender",
                        "street", "city", "state", "zip", "country",
                        "password"]
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
        rates_list = ship.select_rate(
            request.form['origin_add1'],
            request.form['origin_add2'],
            request.form['origin_city'],
            request.form['origin_state'],
            request.form['origin_country'],
            request.form['origin_zip'],
            request.form['origin_phone'],
            request.form['dest_add1'],
            request.form['dest_add2'],
            request.form['dest_city'],
            request.form['dest_state'],
            request.form['dest_country'],
            request.form['dest_zip'],
            request.form['dest_phone'],
            request.form['weight'], request.form['height'],
            request.form['width'], request.form['length'])
        rates_dict = {'rates': rates_list}
        return app.response_class(status=201,
                                  response=json.dumps(rates_dict),
                                  mimetype='application/json')

### ADDS PACKAGE ###
# purchases and records purchase of package
# returns package label information


@app.route('/buylabel/', methods=['POST'])
def addpackage():
    user_id = request.form['user_id']
    rate_id = request.form['rate_id']
    shipment_id = request.form['shipment_id']
    resp = ship.buy_label(shipment_id, rate_id)
    query = f"INSERT INTO labels VALUES (\'{user_id}\', \'{shipment_id}\')"
    return_dict = {'label': resp.postage_label.label_url,
                   'tracker': resp.tracker.id}
    success_check = inter.execute_query(query)
    if success_check:
        return app.response_class(status=200, response=json.dumps(return_dict),
                                  mimetype='application/json')
    else:
        return app.response_class(status=500)


### DELETE PACKAGE ###
@app.route('/deletepackage/', methods=['POST'])
def delete_package():
    package_id = request.form['package_id']
    if ship.delete_package(package_id):
        return app.response_class(status=200)
    else:
        return app.response_class(status=500)


### RETURN THE CARD OPTIONS FOR A GIVEN USER ###
@app.route('/cardoptions/', methods=['POST'])
def card_options():
    userid = request.form["userid"]
    sources = pay.get_card_options(userid)
    return app.response_class(status=200, response=json.dumps(sources),
                              mimetype='application/json')


### ADD CREDIT CARD TO USER'S STRIPE ACCOUNT ###
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
        print(resp)
        return app.response_class(status=200, response=json.dumps(resp),
                                  mimetype='application/json')


### CHARGE THE CARD STORED IN STRIPE ###
@app.route('/chargecard/', methods=['POST'])
def charge_card():
    if request.method == 'POST':
        amount = request.form["amount"]
        resp = pay.charge_card(amount)
        return app.response_class(status=200, response=json.dumps(resp),
                                  mimetype='application/json')


### SEND RECOVERY CODE AND UPDATE CODE IN TABLE ###
@app.route('/sendcode/', methods=['POST'])
def send_email():
    email = request.form['email']
    userid = request.form['userid']
    if inter.user_exists(email, "email"):
        resp = mail.send_code(email, userid)
        if resp:
            return app.response_class(status=200)
        else:
            return app.response_class(status=500)
    else:
        return app.response_class(status=404)


@app.route('/recoverycheck/', methods=['POST'])
def recovery_check():
    userid = request.form["id"]
    code = request.form["code"]
    if inter.code_check(code, userid):
        return app.response_class(status=200)
    else:
        return app.response_class(status=500)


@app.route('/sendlabel/', methods=['POST'])
def send_label():
    if request.method == 'POST':
        email = request.form["email"]
        url = request.form["url"]
        if mail.send_url(email, url):
            return app.response_class(status=200)
        else:
            return app.response_class(status=500)
# return payment method
# create/charge card
# sudo service apache2 restart
# cat /var/log/apache2/error.log
