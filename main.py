import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from datetime import datetime
import datetime
import uuid
from services import firestore_services
import incrementor
import time

embedding_method = "tfidf"
linkge_method = "weighted"
d_metric = "cosine"
d_threshod = 0.8
multiplier = 0.75
new_sentence = "Wearing mask is very necessary is reported by New York"
new_id = 123
fs = firestore_services.FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")


def get_last_tweet_id():
    data = pd.read_csv("data_to_use.csv")
    last_tweet = data.iloc[0]
    last_tweet_id = last_tweet["tweet_id"]
    return last_tweet_id

def get_new_tweets(last_tweet_id):
    last_tweet_snapshot = fs.get_tweet_snapshot_by_id(last_tweet_id)
    return fs.get_newcoming_tweets_since_document_by_snapshot(last_tweet_snapshot)



def get_newsgroup_id_for_news(cluster_id, newcomer_date):
    data = pd. read_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")
    ng_of_cls_id = data.where(data["cluster_id"] == cluster_id)
    ng_of_cls_id = ng_of_cls_id.sort_values(by=["date"], ascending=False)
    last_ng_of_cluster = ng_of_cls_id.iloc[0]
    # dt = datetime.now()
    # dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt = newcomer_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if last_ng_of_cluster.loc["date"] < str(dt):
        return None
    return last_ng_of_cluster["newsgroup_id"]

def create_cluster(tweet_id):
    cluster_id = uuid.uuid1()
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None)
    new_cluster = pd.DataFrame([cluster_id, tweet_id])
    cluster_data = cluster_data.append(new_cluster)
    cluster_data.to_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header = False, index=False)
    return cluster_id

def create_newsgroup(cluster_id, tweet):
    newsgroup_id = uuid.uuid1()
    data = pd. read_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")
    new_newsgroup_local = {
        "newsgroup_id": newsgroup_id,
        "cluster_id": cluster_id,
        "date": tweet["date"]
    }
    new_newsgroup_local = pd.DataFrame(new_newsgroup_local)
    data = data.append(new_newsgroup_local)
    data.to_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")

    new_newsgroup_db = {
        "date": tweet["date"],
        "group_leader": tweet["username"]
        # ----------------------NEED TO BE FILLED--------------------------
    }
    fs.create_newsgroup(new_newsgroup_db, newsgroup_id)

def assign_news_to_cluster(cluster_id, tweet_id):
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None)
    new_cluster = pd.DataFrame([cluster_id, tweet_id])
    cluster_data = cluster_data.append(new_cluster)
    cluster_data.to_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=False, index=False)


def update_tweet(tweet_id, newsgroup_id):
    return None

def save_newcomer_to_local(newcomer):
    return None


def main():
    last_tweet_id = get_last_tweet_id()
    newcoming_news = get_new_tweets(last_tweet_id)
    for snapshot in newcoming_news:
        newcomer = snapshot.to_dict()
        if newcomer["tweet_id"] == last_tweet_id:
            continue
        cluster_id = incrementor.perform(embedding_method, linkge_method, d_metric, d_threshod, multiplier, newcomer["text"], newcomer["tweet_id"])
        if cluster_id is None:
            new_cluster_id = create_cluster(newcomer["tweet_id"])
            newsgroup_id = create_newsgroup(new_cluster_id, newcomer)
        else:
            assign_news_to_cluster(cluster_id, newcomer["tweet_id"])
            newsgroup_id = get_newsgroup_id_for_news(cluster_id, newcomer["date"])
            if newsgroup_id is None:
                newsgroup_id = create_newsgroup(cluster_id, newcomer)
        update_tweet(newcomer["tweet_id"], newsgroup_id)
        save_newcomer_to_local(newcomer)

while True:
    main()
    time.sleep(1)





    # local_data = pd.read_csv("data_to_use.csv")
    # last_tweet_id = local_data.loc[0]["tweet_id"]
    # # print(last_date_ts)
    # query = tweets_ref.where(u"tweet_id", u">", str(last_tweet_id))
    # snaphots = query.stream()
    # # snaphots = tweets_ref.stream()
    # c = 0
    # for i in snaphots:
    #     c += 1
    # print(c)

    # print(last_date)
main()