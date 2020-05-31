import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import firestore as fs


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

    def update_for_newcomer(self, tweet_dict, newsgroup_id, create_newsgroup_firestore):
        transaction = self.db.transaction()
        update_for_newcomer_transactional(transaction, self.db, tweet_dict, newsgroup_id, create_newsgroup_firestore)


@fs.transactional
def update_for_newcomer_transactional(transaction, db, tweet_dict, newsgroup_id, create_newsgroup_firestore):
    newsgroup_ref = db.collection(u"news_groups").document(str(newsgroup_id))
    news_tag = "slow_poke"  # used for updating tag of newcomer and tag count of account
    new_member = 0  # used for setting membership count of account

    # Get tweet
    # tweet_snapshots = db.collection(u"tweets").where(u"tweet_id", "==", str(tweet_id)).stream()
    # tweet_ref = None
    # tweet_dict = None
    # for snapshot in tweet_snapshots:
    #     tweet_ref = snapshot.reference
    #     tweet_dict = snapshot.to_dict()
    #     break
    tweet_ref = tweet_dict["document_reference"]

    # Read Account Document
    account_ref = db.collection(u"accounts").document(tweet_dict["username"])
    account_data = account_ref.get(transaction=transaction).to_dict()

    # update newsgroup document
    if create_newsgroup_firestore:  # a new newsgroup created
        merge = True
        news_tag = "first_reporter"
        new_member = 1
        source_count_map = dict()
        category_map = dict()
        first_reporter_map = dict()
        close_second_map = dict()
        late_comer_map = dict()
        slow_poke_map = dict()
        follow_up_map = dict()
        source_count_map[tweet_dict["username"]] = 1
        category_map[tweet_dict["category"]] = 1
        first_reporter_map[tweet_dict["username"]] = 1

        data_to_update = {
            u'count': 1,
            u'is_active': True,
            u'group_leader': tweet_dict["username"],
            u'source_count_map': source_count_map,
            u'category_map': category_map,
            u'first_reporter_map': first_reporter_map,
            u'close_second_map': close_second_map,
            u'late_comer_map': late_comer_map,
            u'slow_poke_map': slow_poke_map,
            u'follow_up_map': follow_up_map,
            u'category': tweet_dict["category"],
            u'updated_at': tweet_dict["date"],
            u'created_at': tweet_dict["date"],
            u'first_reporter': tweet_ref.id,
            u'close_second': "",
            u'late_comer': "",
            u'slow_poke': "",
            u'follow_up': ""
        }
        
    else:  # the newsgroup already exists
        # Read Newsgroup Document
        newsgroup_data = newsgroup_ref.get(transaction=transaction).to_dict()
        source_count_map = newsgroup_data["source_count_map"]
        category_map = newsgroup_data["category_map"]
        merge = False

        # Update Source Count Map and assign a news tag to News
        if tweet_dict["username"] in source_count_map:  # if account already posted news
            news_tag = "follow_up"
            source_count_map[tweet_dict["username"]] += 1
        else:  # if this is the first news for account
            merge = True
            new_member = 1
            count = len(source_count_map.keys())
            if count == 1:
                news_tag = "close_second"
            elif count == 2:
                news_tag = "late_comer"
            source_count_map[tweet_dict["username"]] = 1

        # Update Category Map and Perceived Category of NewsGroup
        perceived_category = newsgroup_data["category"]

        if tweet_dict["category"] in category_map:
            category_map[tweet_dict["category"]] += 1
        else:
            merge = True
            category_map[tweet_dict["category"]] = 1

        if (category_map[perceived_category] < category_map[tweet_dict["category"]]) or (
                perceived_category == "-" and category_map[perceived_category] == category_map[tweet_dict["category"]]):
            perceived_category = tweet_dict["category"]

        tag_map_key = news_tag + "_map"
        tag_map = newsgroup_data[tag_map_key]

        if tweet_dict["username"] in tag_map:
            tag_map[tweet_dict["username"]] += 1
        else:
            merge = True
            tag_map[tweet_dict["username"]] = 1

        data_to_update = {
            u'count': newsgroup_data["count"] + 1,
            u'source_count_map': source_count_map,
            u'category_map': category_map,
            u'category': perceived_category,
            u'updated_at': tweet_dict["date"],
            f"{news_tag}": tweet_ref.id,
            f"{tag_map_key}": tag_map,
        }

    # update Tweet Document
    transaction.update(tweet_ref, {u"news_group_id": str(newsgroup_id)})

    # update Newsgroup Document
    if merge:
        transaction.set(newsgroup_ref, data_to_update, merge=True)
    else:
        transaction.update(newsgroup_ref, data_to_update)

    # update Account Document
    transaction.update(account_ref, {
        u'news_count': account_data["news_count"] + 1,
        u'news_group_membership_count': account_data["news_group_membership_count"] + new_member,
        f"{news_tag}": account_data[news_tag] + 1
    })


def add_tweet(self, tweet):
    self.db.collection('tweets').document().set(tweet)
