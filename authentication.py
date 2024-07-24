import pyrebase

config = {
    'apiKey': "AIzaSyCWM-vCsE97Cf0Bb4K6vY9k3Rd9T4NQl9k",
    'authDomain': "loginwebdst.firebaseapp.com",
    'projectId': "loginwebdst",
    'storageBucket': "loginwebdst.appspot.com",
    'messagingSenderId': "325449546203",
    'appId': "1:325449546203:web:92d912967054e3ba8e8ffe",
    'measurementId': "G-X0KYG3T1E2",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = '12345678'

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)
#print(user)

info = auth.get_account_info(user['idToken'])
print(info)

#auth.send_email_verification(user['idToken'])
#auth.send_password_reset_email(email)