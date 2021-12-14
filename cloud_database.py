import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
cred = credentials.Certificate("ijeoma-f45f5-firebase-adminsdk-8zknw-ec62869267.json")
firebase_admin.initialize_app(cred)




bucket = storage.bucket(name="ijeoma-f45f5.appspot.com")
blob = bucket.blob('images/file1.jpg')
path="orabel.jpg"
blob.upload_from_filename(path)

# bucket = storage.bucket()
# blob = bucket.blob('/imageName')
# imagePath = "/Users/name/Desktop/IMG_1895.jpg"
# blob.upload_from_filename(imagePath)