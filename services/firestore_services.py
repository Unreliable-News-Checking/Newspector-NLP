import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

class FireStoreServices(object):

    def __init__(self, credentials_resource):
        self.cred = credentials.Certificate(credentials_resource)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def create_newsgroup(self, dic, id):
        self.db.collection("newsgroups").document(str(id)).set(dic)

    def get_tweet_snapshot_by_id(self, id):
        snapshots = self.db.collection("tweets").where(u"tweet_id", "==", str(id)).stream()
        for s in snapshots:
            return s

    def get_newcoming_tweets_since_document_by_snapshot(self, document_snapshot):
        return self.db.collection(u'tweets').order_by(u'date').start_at(document_snapshot).get()

    def get_newcoming_tweets_since_date(self, date):
        return self.db.collection(u'tweets').order_by(u'date').where(u"date", ">", int(date)).stream()

    def update_for_newcomer(self, tweet_id, newsgroup_id, newsgroup_data):
        # print(newsgroup_data)
        batch = self.db.batch()
        if newsgroup_data is not None:
            newsgroup_ref = self.db.collection(u"news_groups").document(str(newsgroup_id))
            batch.set(newsgroup_ref, newsgroup_data)
        tweet_snapshots = self.db.collection(u"tweets").where(u"tweet_id", "==", str(tweet_id)).stream()
        # tweet_snapshots = self.db.collection(u"tweets").where(u"tweet_id", "==", tweet_id).stream()
        tweet_ref = None
        for snapshot in tweet_snapshots:
            tweet_ref = snapshot.reference
            break
        batch.update(tweet_ref, {u"news_group_id": str(newsgroup_id)})
        batch.commit()

    def add_tweet(self, tweet):
        self.db.collection('tweets').document().set(tweet)
