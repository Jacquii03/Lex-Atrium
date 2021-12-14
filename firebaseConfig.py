import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("ijeoma-f45f5-firebase-adminsdk-8zknw-ec62869267.json")
firebase_admin.initialize_app(cred)



