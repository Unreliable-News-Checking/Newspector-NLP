import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

class FireStoreServices(object):

    def __init__(self, credentials_resource):
        self.cred = credentials.Certificate(credentials_resource)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

fss = FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")

data = pd. read_csv("clusters_newsgroups/tfidf_weighted_cosine_0.8.csv")
print(data.shape)

collection = fss.db.collection('news_groups')
documents = list(collection.get())
print("# of documents in collection: {}".format(len(documents)))

