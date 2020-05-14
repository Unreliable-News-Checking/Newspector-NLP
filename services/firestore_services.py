import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore
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

    @firestore.transactional
    def update_for_newcomer(self, tweet_id, newsgroup_id, newsgroup_data):
        transaction = self.db.transaction()
        newsgroup_ref = self.db.collection(u"news_groups").document(str(newsgroup_id))
        news_tag = "slow_poke"  # used for updating tag of newcomer and tag count of account
        new_member = 0  # used for setting membership count of account

        # update tweet
        tweet_snapshots = self.db.collection(u"tweets").where(u"tweet_id", "==", str(tweet_id)).stream()
        tweet_ref = None
        for snapshot in tweet_snapshots:
            tweet_ref = snapshot.reference
            break
        transaction.update(tweet_ref, {u"news_group_id": str(newsgroup_id)})

        # update newsgroup document
        if newsgroup_data is not None:  # a new newsgroup created
            news_tag = "first_reporter"
            new_member = 1
            newsgroup_data["count"] = 1
            newsgroup_data["source_count_map"][tweet_ref["username"]] = 1
            newsgroup_data["category_map"][tweet_ref["category"]] = 1
            newsgroup_data["category"] = tweet_ref["category"]
            newsgroup_data[news_tag] = tweet_ref["id"]
            transaction.set(newsgroup_ref, newsgroup_data)
        else:
            newsgroup_data = newsgroup_ref.get(transaction=transaction).to_dict()
            source_count_map = newsgroup_data["source_count_map"]
            category_map = newsgroup_data["category_map"]
            merge = False

            # Update Source Count Map and assign a news tag to News
            if tweet_ref["username"] in source_count_map:  # if account already posted news
                news_tag = "follow_up"
                source_count_map[tweet_ref["username"]] += 1
            else:  # if this is the first news for account
                merge = True
                new_member = 1
                count = newsgroup_data["count"]
                if count == 1:
                    news_tag = "close_second"
                elif count == 2:
                    news_tag = "late_comer"
                source_count_map[tweet_ref["username"]] = 1

            # Update Category Map and Perceived Category of NewsGroup
            perceived_category = newsgroup_data["category"]

            if tweet_ref["category"] in category_map:
                category_map[tweet_ref["category"]] += 1
            else:
                merge = True
                category_map[tweet_ref["category"]] = 1

            if (category_map[perceived_category] < category_map[tweet_ref["category"]]) or (
                    perceived_category == "-" and category_map[perceived_category] == category_map[tweet_ref["category"]]):
                perceived_category = tweet_ref["category"]

            data_to_update = {
                    u'count': newsgroup_data["count"] + 1,
                    u'source_count_map': source_count_map,
                    u'category_map': category_map,
                    u'category': perceived_category,
                    u'updated_at': tweet_ref["date"],
                    [news_tag]: tweet_ref["id"]
                }

            if merge:
                transaction.set(newsgroup_ref, data_to_update, merge=True)
            else:
                transaction.update(newsgroup_ref, data_to_update)

        # update account
        account_ref = self.db.collection(u"accounts").document(tweet_ref["username"])
        account_data = account_ref.get(transaction=transaction).to_dict()
        transaction.update(account_ref, {
            u'news_count': account_data["news_count"] + 1,
            u'news_group_membership_count': account_data["news_group_membership_count"] + new_member,
            [news_tag]: account_data[news_tag] + 1
        })

    def add_tweet(self, tweet):
        self.db.collection('tweets').document().set(tweet)
