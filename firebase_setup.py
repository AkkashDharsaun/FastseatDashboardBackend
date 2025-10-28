import firebase_admin
from firebase_admin import credentials, db, storage

# Load service account key
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    "storageBucket": "seat-checking-app.appspot.com",  # ✅ correct bucket format
    "databaseURL": "https://fastseat-74d7f-default-rtdb.firebaseio.com"
})

# Get default bucket instance
bucket = storage.bucket()
print("Database URL:", db.reference().path)
print("Bucket Name:", bucket.name)
