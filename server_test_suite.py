import requests

# returns 'user already exists'
# use requests.post('http://127.0.0.1:5000/user/', data = input_user)
input_user = {'username': 'donatellaversace', 'email': 'tellabella@aol.com',
              'sender_name': 'Donatella_Versace', 'sender_street': '8008 18th Ave',
              'sender_city': 'Seattle', 'sender_state': 'Washington',
              'sender_zip': 98115, 'sender_country': 'USA', 'password':
              't00nafEEsh!11'}

# returns valid user
# use requests.get('http://127.0.0.1:5000/user/', data = input_user)
input_user_true = {'username': 'donatellaversace'}
# returns 'user does not exist'
input_user_false = {'username': 'douglasfur'}

# deletes user (make sure user has been created first)
# requests.delete('http://127.0.0.1:5000/user/', data = input_user_delete)
# requests.get('http://127.0.0.1:5000/user/', data = input_user_delete)
# should return "user does not exist"
input_user_delete = {'username': 'donatellaversace'}


# modify user test, returns 'user updated'
# use requests.put('http://127.0.0.1:5000/usermod/email/', data=modify_email)
modify_email = {'id': 1, 'email': 'tellybelly@aol.com'}
modify_password = {'id': 1, 'password': 'jellybelly99'}
modify_false = {'id': 50, 'email': 'nobody@gmail.com'}

# get user id, returns '1'
# use requests.get('http://127.0.0.1:5000/checkident/', data=input_email)
input_email = {'email': 'tellabella@aol.com'}

# test shipping capabilities: true does not return error, false returns error
# requests.post('http://127.0.0.1:5000/addpackage/', data=shipping_input)
shipping_input_parcel = {'userid': 1, 'dest_name': 'Mr. Reciever',
                         'dest_street': '1115 8th Ave', 'dest_city':
                         'Grinnell', 'dest_state': 'Iowa', 'dest_zip': '50112',
                         'dest_country': 'USA', 'length': 12, 'width': 6.5,
                         'height': 12.5, 'weight': 15}

shipping_input_flat_rate = {'userid': 1, 'dest_name': 'Mr. Reciever',
                            'dest_street': '1115 8th Ave', 'dest_city':
                            'Grinnell', 'dest_state': 'Iowa', 'dest_zip':
                            '50112', 'dest_country': 'USA',
                            'predefined_package': 'FlatRateEnvelope',
                            'weight': 15}

shipping_input_false = {'userid': 1, 'dest_name': 'Miss Nobody',
                        'dest_street': '4444 444th Ave', 'dest_city':
                        'Santa Fe', 'dest_state': 'New Mexico', 'dest_zip':
                        '44444', 'dest_country': 'USA', 'length': 12, 'width':
                        6.5, 'height': 12.22, 'weight': 15}

# test password validation
# requests.post('http://127.0.0.1:5000/validate/', validate_user)
# returns 200 if passwords match, 406 if not
validate_user = {'username': 'donatellaversace', 'password': 't00nafEEsh!11'}


# get each user package in the form of a list of dictionaries
# when retrieving each package, use response.json()[0] or the
# flutter equivalent
# requests.post('http://127.0.0.1:5000/previouspackages/1/')
# shoul return dict object, data=user_packages_false should not
user_packages_true = {'id': 1}
user_packages_false = {'id': 2}

requests.post('http://127.0.0.1:5000/user/', data=input_user)
resp = requests.post('http://127.0.0.1:5000/addpackage/',
                     data=shipping_input_flat_rate)
print(resp.content)
