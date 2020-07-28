import requests
import json

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
# use requests.get('http://127.0.0.1:5000/identuser/', data=input_email)
input_email = {'email': 'tellabella@aol.com'}

# test out the function of getting rates by sending package details and
# recieving the shipping rate options (choose rate in separate function)
# requests.post('http://127.0.0.1:5000/getrates/, data=rate_input)
rate_input_true = {'origin_country': 'US', 'origin_zip': '98115',
                   'origin_city': 'Seattle', 'origin_state': 'WA', 'dest_city':
                   'Grinnell', 'dest_state': 'IA', 'dest_country': 'US',
                   'dest_zip': '50112', 'tax_payer': 'Sender', 'insured':
                   'false', 'weight': 15, 'height': 12.5, 'width': 6.5,
                   'length': 12, 'category': 'fashion', 'currency': 'USD',
                   'customs_val': 35}

rate_input_false = {'origin_country': 'US', 'origin_zip': '98115',
                    'origin_city': 'Seattle', 'origin_state': 'WA',
                    'dest_city': 'Grinnell', 'dest_state': 'IA',
                    'dest_country': 'US', 'dest_zip': '', 'tax_payer':
                    'Sender', 'insured': 'false', 'weight': -15,
                    'height': 12.5, 'width': 6.5, 'length': 12, 'category':
                    'fashion', 'currency': 'USD', 'customs_val': 35}


# test shipping capabilities: true does not return error, false returns error
# requests.post('http://127.0.0.1:5000/addpackage/', data=shipping_input)
shipping_input_true = {'platform_name': 'Amazon',
                       'platform_order_number': '#1',
                       'user_id': 1, 'dest_name': 'Mr. Reciever',
                       'dest_add1': '1115 8th Ave', 'dest_add2': '',
                       'dest_city': 'Grinnell', 'dest_state': 'IA',
                       'dest_zip': '50112', 'dest_country': 'US',
                       'dest_phone': '+1 206-867-5309', 'dest_email':
                       'ecl.damoose@gmail.com', 'item_description':
                       'cat rain boots', 'weight': 15.23, 'height': 12.5,
                       'width': 6.5, 'length': 12, 'category': 'fashion',
                       'currency': 'USD', 'customs_val': 35.01,
                       'courier_id': '2bd30fb9-8f41-4fc3-950d-3675494ae318'}

shipping_input_false = {'user_id': 1, 'dest_name': 'Mr. Reciever',
                        'dest_add1': '1115 8th Ave', 'dest_add2': '',
                        'dest_city': 'Grinnell', 'dest_state': 'IA',
                        'dest_zip': '50112', 'dest_country': 'US',
                        'dest_phone': '+1 206-867-5309', 'dest_email':
                        'ecl.damoose@gmail.com', 'item_description':
                        'cat rain boots', 'weight': 15, 'height': -12.5,
                        'width': 6.5, 'length': 12, 'category': 'fashion',
                        'currency': 'USD', 'customs_val': 35,
                        'courier_id': '2b18'}

shipping_purchase_test = {'user_id': 1, 'dest_name': 'Mr. Reciever',
                          'dest_add1': '11', 'dest_add2': '',
                          'dest_city': 'Grinnell', 'dest_state': 'IA',
                          'dest_zip': '50112', 'dest_country': 'US',
                          'dest_phone': '+1 206-867-5309', 'dest_email':
                          'ecl.damoose@gmail.com', 'item_description':
                          'cat rain boots', 'weight': 15, 'height': -12.5,
                          'width': 6.5, 'length': 12, 'category': 'fashion',
                          'currency': 'USD', 'customs_val': 35,
                          'courier_id': '2bd30fb9-8f41-4fc3-950d-3675494ae318'}


# shipment deletion test
# request.delete(http://127.0.0.1:5000/deletepackage/,data=package_delete_true)
package_delete_false = {'shipmentid': 'ESUS10035316'}


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


# retrieve all past packages for a given user
# requests.get('http://127.0.0.1:5000/getpackages/{userid}/')


# test stripe payment capabilities
stripe_true = {'cost': 123}
stripe_false = {'cost': -123}


# resp = requests.post('http://127.0.0.1:5000/getpackages/addpayment/',
#                       data=payment_true)
payment_true = {'default': 'True', 'customerid': 'cus_HhgZBY5XFfoZwW',
                'payment_method': 'pm_1H8GojAzJnRyZcvUeAMXzRZW'}


# resp = requests.post('http://127.0.0.1:5000/addpayment/',
#                      data=create_payment_method)
create_payment_method = {'default': 'False', 'card_num': '4242424242424242',
                         'cvc': '314', 'exp_month': 7, 'exp_year': 2021,
                         'stripeid': 'cus_Hj7qZ7KnMgUquT'}


charge_card = {'payment_token': 'pm_1H9yYXAzJnRyZcvUNdL1Sa6H', 'amount': 123.4}



print(resp.content)
