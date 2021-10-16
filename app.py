import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import datetime

class user():
    def __init__(self):
        # sets username and password to session
        self.user_name = None
        self.password = None
        # firebase credentials
        self.cred = credentials.Certificate('/Users/densmoreb/Documents/myprojects/cloud_project/activities-296f9-firebase-adminsdk-22lk4-ea227fb9e2.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        # self.bucket = storage.Bucket('gs://activities-296f9.appspot.com/')
        # self.blob = self.bucket.blob('/3a83ea6f-8934-402a-a59b-694f81612ba3-PLANTERONI_OV_PULL_002.jpg.webp')
        # print(self.blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))



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


# login
    def login(self):
        self.user_name = input('username: ')
        self.password = input('password: ')
        
        check_user = self.db.collection('users').document(self.user_name).get()
        if not check_user.exists:
            print('does not exist')
            print('must create user')
            self.create_user()

        results = self.db.collection('users').where('password', '==', self.password).get()
        if len(results) == 0:
            print('invalid password')
        else:
            print('sucessful login')
            # self.select_activ()
            # self.show_activites()
            self.main_menu()


    def select_activ(self):
        """
        Select activites one at a time with an option of yes or no saving their pick to their username
        """
        docs = self.db.collection('activities').get()
        count = 0
        for item in docs:
            dict = item.to_dict()
            print(f"Name: {dict['name']} Address: {dict['address']} Price: ${dict['price']}")
            count += 1
            if count > 0:
                choice = input('y or n? ')
                if choice == 'y':
                    liked_act = {
                        'activity id' : item.id,
                        'username' : self.user_name
                    }
                    self.db.collection('liked_activities').add(liked_act)

    def show_activites(self):
        """
        Shows the activities that are matched between users
        """

        other_user = input('Who would you like to match with? \n')

        other_act_id = self.db.collection('liked_activities').where('username', '==', other_user).get()
        liked_act_id = self.db.collection('liked_activities').where('username', '==', self.user_name).get()
        docs = self.db.collection('activities').get()
        
        print('\nTheir activities:')
        for item in other_act_id:
            other_dict = item.to_dict()
            id = other_dict['activity id']

            for i in docs:
                name = i.to_dict()
                if i.id == id:
                    print(f"Name: {name['name']}, Address: {name['address']}, Price: ${name['price']}")
        
        print('\nYour activities:')
        for item in liked_act_id:
            liked_dict = item.to_dict()
            id = liked_dict['activity id']

            for i in docs:
                name = i.to_dict()
                if i.id == id:
                    print(f"Name: {name['name']}, Address: {name['address']}, Price: ${name['price']}")

                    

    def main_menu(self):
        print('Welcome to your Date Night')
        choice = None
        while choice != 'q':
            choice = input('What would you like to do? show liked activites(s), like activites(l), or quit(q) ')
            if choice == 's':
                self.show_activites()
            elif choice == 'l':
                self.select_activ()
            elif choice == 'q':
                quit()
            else:
                print('wrong input ')



db_user = user()
db_user.login()
