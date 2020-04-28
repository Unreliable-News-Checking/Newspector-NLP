import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

class FireStoreServices(object):

    def __init__(self, credentials_resource):
        self.cred = credentials.Certificate(credentials_resource)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

fss = FireStoreServices("service-account-file.json")
users_ref = fss.db.collection(u'train_tweets').order_by(
    u'date', direction=firestore.Query.DESCENDING).limit(2000)
tweetSnapshots = users_ref.stream()

tweets = []
for tweetSnapshot in tweetSnapshots:
    tweets.append(tweetSnapshot.to_dict())

df = pd. DataFrame(tweets)
df.to_csv("tweets2.csv")