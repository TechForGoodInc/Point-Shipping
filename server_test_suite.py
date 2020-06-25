import requests

# returns 'user already exists'
# use requests.post('http://127.0.0.1:5000/user/', data = input_data)
input_data = {'username': 'donatellaversace', 'firstname': 'Donatella',
              'lastname': 'Versace', 'email': 'tellabella@aol.com',
              'address': '1115_None_of_Your_Business_St', 'password': 't00nafish'}

# returns valid user
# use requests.get('http://127.0.0.1:5000/user/', data = input_user)
input_user_true = {'username': 'donatellaversace'}
# returns 'user does not exist'
input_user_false = {'username': 'douglasfur'}

# modify user test, returns 'user updated'
# use requests.put('http://127.0.0.1:5000/usermod/email/', data=modify_column)
modify_column = {'id': 2, 'email': 'tellabella@aol.com'}

input_email = {'email': 'tellybelly@aol.com'}

response = requests.get(
    'http://127.0.0.1:5000/identuser/',
    data=input_email
)

print(response.content)

