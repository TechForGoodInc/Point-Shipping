import pyrebase
import firebase_admin
from firebase_admin import credentials
import interface as inter

firebaseConfig = {
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
  # CHANGE SERVICE ACCOUNT ID ON SERVER

# __Admin__ google account used to login in firebase, I already sign him up
# Email: tech0493@gmail.com
# pass: Tech123456


# create a new user
def signUpNewUser(email, password):
    firebase = pyrebase.initialize_app(firebaseConfig)
    authen = firebase.auth()
    new_User = authen.create_user_with_email_and_password(email, password)
    return new_User


data = ["candy@gmail.com", "cookie"]


# allow the user to sign into the account
# NEEDS TESTING
def login(email, password):
    if inter.user_exists(email, "email"):
        firebase = pyrebase.initialize_app(firebaseConfig)
        authen = firebase.auth()
        user = authen.sign_in_with_email_and_password(email, password)
        print(db.child(user).get())
        return user['email']
    else:
        return False


# retrevieve the data using the get method
def retreiveData():
    firebase = pyrebase.initialize_app(firebaseConfig)
    authen = firebase.auth()
    db = firebase.database()
    user = db.child("candy@gmail.com").get()
    print(user)
    return user
# adds data to the database


retreiveData()


def pushData():
    firebase = pyrebase.initialize_app(firebaseConfig)
    authen = firebase.auth()
    db = firebase.database()
    db.child("user").push(data)
    print(data)
    print("User info added")
    return 1


# remove user
def removeU():
    firebase = pyrebase.initialize_app(firebaseConfig)
    authen = firebase.auth()
    db = firebase.database()
    db.child("user").child("key").remove()
    print("User removed!")
    return 1