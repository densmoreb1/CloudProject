import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class user():
    def __init__(self):
        # sets username and password to session
        self.user_name = None
        self.password = None
        # firebase credentials
        self.cred = credentials.Certificate('/Users/densmoreb/Documents/myprojects/cloud_project/activities-296f9-firebase-adminsdk-22lk4-ea227fb9e2.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()


# insert activites
    def insert_activ(self):
        """ 
        This function is really only for the admin to enter all the data into the cloud. 
        This is not to be used by the users.
        """
        file_name = os.path.join(os.path.abspath('activites.json'))
        json_file = json.load(open(file_name))
        for majorkey, subdict in json_file.items():
            doc = self.db.collection('activities').document(majorkey)
            doc.set(subdict)


# select activites one at a time with an option of yes or no saving their pick to their username
    def select_activ(self):
        docs = self.db.collection('activities').get()
        count = 0
        for item in docs:
            dict = item.to_dict()
            print(f"Name: {dict['name']} Address: {dict['address']} Price: ${dict['price']}")
            count += 1
            if count > 0:
                input('y or n? ')

# login
    def login(self):
        self.user_name = input('username: ')
        self.password = input('password: ')
        results = self.db.collection('users').where('password', '==', self.password).get()
        for result in results:
            item = result.to_dict()
            print(item)
            

# create user
    def create_user(self):
        self.user_name = input('username: ')
        self.password = input('password: ')
        first_name = input('first name: ')
        last_name = input('last name: ')
        info = {
            "first name": first_name,
            "last name": last_name,
            "password": self.password
        }

        self.db.collection('users').document(self.user_name).set(info)

db_user = user()
db_user.login()