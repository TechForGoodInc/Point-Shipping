import requests

# returns 'user already exists'
# use requests.post('http://127.0.0.1:5000/user/', data = input_data)
input_user = {'username': 'donatellaversace', 'email': 'tellabella@aol.com',
              'sender_name': 'Donatella_Versace', 'sender_street': '22nd',
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

# test shipping capabilities
# requests.post('http://127.0.0.1:5000/addpackage/', data=shipping_input)
shipping_input = {'userid': 1, 'dest_name': '1234', 'dest_street': '19th Ave',
                  'dest_city': 'Santa Fe', 'dest_state': 'New Mexico',
                  'dest_zip': '87501', 'dest_country': 'USA', 'length': 12,
                  'width': 6.5, 'height': 12.22, 'weight': 15}

# test password validation
# requests.get('http://127.0.0.1:5000/validate/)
# returns 200 if passwords match, 406 if not
validate_user = {'userid': 1, 'password': 't00nafEEsh!11'}

requests.post('http://127.0.0.1:5000/addpackage/', data=shipping_input)
