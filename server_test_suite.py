import requests

input_data = {'username': 'emilylouden', 'firstname': 'Emily',
              'lastname': 'Louden', 'email': 'emilylouden@techforgoodinc.org',
              'address': 'P_Sherman_Wallaby_Way', 'password': 'passw00rd!'}

response = requests.post(
    'http://127.0.0.1:5000/user/',
    data=input_data,
)

print(response.content)

