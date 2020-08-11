import pyrebase
import firebase_admin
from firebase_admin import credentials
import interface as inter

firebase_config = {
    "apiKey": "AIzaSyBEjDWngQQAqT1ChTrbw_55bW_Di_X1c7o",
    "authDomain": "shippingpoint-01.firebaseapp.com",
    "databaseURL": "https://shippingpoint-01.firebaseio.com",
    "projectId": "shippingpoint-01",
    "storageBucket": "shippingpoint-01.appspot.com",
    "messagingSenderId": "1077762885942",
    "appId": "1:1077762885942:web:c69aa0d904ef08bb400b97",
    "measurementId": "G-MY4XZT7978",
    "serviceAccount": "/Users/emilylouden/Desktop/fork-11/modules/service_id.json"
  }

# CHANGE SERVICE ACCOUNT ID PATH ON SERVER

# __Admin__ google account used to login in firebase, I already sign him up
# Email: tech0493@gmail.com
# pass: Tech123456


# create a new user
def sign_up_new_user(email, password, userid):
    # if inter.user_exists(email, "email"):
    firebase = pyrebase.initialize_app(firebase_config)
    authen = firebase.auth()
    user = authen.create_user_with_email_and_password(email, password)
    db = firebase.database()
    data = {'userid': userid}
    comma_email = email.replace(".", ",")
    db.child("users").child(comma_email).set(data)
    return True


# allow the user to sign into the account
def login(email, password):
    firebase = pyrebase.initialize_app(firebase_config)
    authen = firebase.auth()
    user = authen.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    comma_email = email.replace(".", ",")
    resp = db.child("users").child(comma_email).get().val()
    return resp['userid']


def remove_user(email):
    firebase = pyrebase.initialize_app(firebase_config)
    authen = firebase.auth()
    db = firebase.database()
    comma_email = email.replace(".", ",")
    db.child("user").child(comma_email).remove()
    return True
