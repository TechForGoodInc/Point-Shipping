import requests

# returns 'user already exists'
# use requests.post('http://127.0.0.1:5000/user/', data = input_data)
input_data = {'username': 'donatellaversace', 'firstname': 'Donatella',
              'lastname': 'Versace', 'email': 'tellabella@aol.com',
              'sender_name': 'Donatella_Versace', 'sender_street': '22nd',
              'sender_city': 'Seattle', 'sender_state': 'Washington',
              'sender_zip': 98115, 'sender_country': 'USA', 'seed': '2b$1',
              'password': '2b$12$RQhfNQCIFEEUX'}

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
modify_email = {'id': 2, 'email': 'tellabella@aol.com'}
modify_password = {'id': 2, 'password': 'jellybelly99'}
modify_false = {'id': 50, 'email': 'nobody@gmail.com'}

# get user id, returns '1'
# use requests.get('http://127.0.0.1:5000/checkident/', data=input_email)
input_email = {'email': 'tellabella@aol.com'}

response = requests.put('http://127.0.0.1:5000/usermod/email/', data=modify_false)


# FIX MODIFY EMAIL
print(response.content)

