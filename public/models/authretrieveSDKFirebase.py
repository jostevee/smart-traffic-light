import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('smart-traffic-light-312914-firebase-adminsdk-3semq-32e815d5d4.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-traffic-light-312914-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
# ref = db.reference('restricted_access/secret_document')
# print(ref.get())

# Get a database reference to our posts
ref = db.reference('ml_mantabs/intersection').get()
print(ref)
# Read the data at the posts reference (this is a blocking operation)

for business in ref:
    print(business.values())

# for user, val in ref.items():  # iterate until number of people in database is reached
#     print(f'\n{val}')  # Print the users values

# snapshot = ref.order_by_child('height').equal_to(25).get()
# for key in snapshot:
#     print(key)