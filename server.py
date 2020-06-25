from flask import Flask, render_template, request, json
import requests
import interface as inter
import shipping as ez

### BASIC INITIALIATION ###
app = Flask(__name__)

if __name__ == '__main__':
    app.run()

### TESTS ###
@app.route('/')
def init():
    rqst = "SELECT * FROM users"
    resp = inter.execute_read_query(rqst)
    to_send = app.response_class(response=json.dumps(resp), status=200,
                                 mimetype='application/json')
    return to_send

### GET, POST, AND DELETE ###
# get recieves data, post sends data
@app.route('/user/', methods=['GET', 'POST', 'DELETE'])
def user():
    user_name = request.form['username']
    if request.method == 'POST':
        user_exist = inter.execute_read_query(f"SELECT COUNT(*) FROM users WHERE username = \'{user_name}\'")
        exist_check = user_exist[0][0]
        max_id = 0
        #max_id = inter.execute_query("SELECT MAX(id) FROM users")
        if exist_check > 0:
            return "User does not exist"
        else:
            idval = max_id + 1
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            addr = request.form['address']
            pswd = request.form['password']
            query = f"""INSERT INTO users VALUES (\'{user_name}\', \'{idval}\',
            \'{firstname}\', \'{lastname}\', \'{email}\', \'{addr}\', \'{pswd}\')"""
            inter.execute_query(query)
            return "User added"
    elif request.method == 'GET':
        query = f"SELECT * FROM users WHERE username = \'{user_name}\'"
        resp = inter.execute_read_query(query)
        if not resp:
            response = app.response_class(response=json.dumps(resp),
                                          status=200,
                                          mimetype='application/json')
            return response
        else:
            response = app.response_class(status=400)
            return response
        # 200 = standard ok status, 400 = user did not exist (client error)

    elif request.method == 'DELETE':
        query = "DELETE FROM users WHERE username = \'{username}\'"
        return inter.execute_read_query(query)


### MODIFY USER ###
# The column name represents what user attribute to update
# ID val is accessible through user identifier method
@app.route('/usermod/<col_name>', methods=['PUT'])
def update_user(col_name):
    idval = request.form['id']
    user_exist = inter.execute_query(f"SELECT COUNT(*) WHERE id = {idval}")
    if user_exist > 0:
        return False
    else:
        replace = request.form[f"\'{col_name}\'"]
        query = f"UPDATE users SET \'{col_name}\' = \'{replace}\' WHERE id = \'{idval}\'"
        inter.execute_query(query)
        return True

### RECOVER ID ###
# Uses user email to recover user attributes. This can be used
# in tandem with the update_user method which takes a user id
@app.route('/identuser/', methods=['GET'])
def identify_user():
    email = request.form['email']
    resp = inter.execute_read_query("SELECT id FROM users WHERE email = \'{email}\'")
    if not resp:
        response = app.response_class(response=json.dumps(resp),
                                      status=200,
                                      mimetype='application/json')
        return response
    else:
        response = app.response_class(status=199)
        return response

@app.route('/validate/', methods=['POST'])
def validate():
    username = request.form['username']
    query = f"SELECT pswd FROM users WHERE username = \'{username}\'"
    resp = inter.execute_read_query(query)
    if not resp:
        response = app.response_class(response=json.dumps(resp),
                                      status=200,
                                      mimetype='application/json')
        return response
    else:
        return False

@app.route('/authorize/', methods=['GET'])
def authorize():
    username = request.form['username']
    query = f"SELECT pswd FROM users WHERE username = \'{username}\'"
    resp = inter.execute_read_query(query)
    if not resp:
        return "user does not exist"
    else:
        if request.form['password'] == resp:
            return "pw verified"
        else:
            return "incorrect pw"


@app.route('/addpackage/', methods=['POST'])
def addpackage(username):

    userid = request.form['userid']

    dest_name = request.form['dest_name']
    dest_street = request.form['dest_street']
    dest_city = request.form['dest_city']
    dest_state = request.form['dest_state']
    dest_zip = request.form['dest_zip']
    dest_country = request.form['dest_country']
    toAddress = ez.get_to_address(dest_name, dest_street, dest_city,
                                  dest_state, dest_zip, dest_country)

    from_name = request.form['from_name']
    from_street = request.form['from_street']
    from_city = request.form['from_city']
    from_state = request.form['form_state']
    from_zip = request.form['from_zip']
    from_country = request.form['from_country']
    fromAddress = ez.get_from_address(from_name, from_street, from_city,
                                      from_state, from_zip, from_country)

    i_length = request.form['length']
    i_width = request.form['width']
    i_height = request.height['height']
    i_weight = request.weight['weight']
    parcel = ez.Parcel.create(length=i_length, width=i_width,
                              height=i_height, weight=i_weight)
    
    send_date = request.form['send_date']

    shipment = ez.Shipment.create(parcelObj=parcel,
                                  to_address=toAddress,
                                  from_address=fromAddress)
    return shipment


@app.route('/previouspackages/<userval>/', methods=['GET'])
def get_packages(userval):
    query = f"SELECT * FROM labels WHERE userid = \'{userval}\'"
    return inter.execute_query(query)

# user checked out and paid for package
# send post request with new shipping label info and username
# return "ok"

# requests.post
