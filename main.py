import pandas as pd
from datetime import datetime
import datetime
import uuid
from services import firestore_services
import incrementor
import time
from services import preprocessing as pre
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

check_freq = 120 #sec
delay = 1 #sec
news_group_lifetime = 48 #hours
news_group_lifetime = news_group_lifetime * 60 * 60 * 1000  #millisecs

embedding_method = "bow"
linkge_method = "average"
d_metric = "cosine"
d_threshod = 0.9
inc_d_threshold = 0.85
multiplier = 0.75
new_sentence = "Wearing mask is very necessary is reported by New York"
new_id = 123
fs = firestore_services.FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")


stop_words = set(stopwords.words('english'))

def preprocess(text):
    # vectors = pd.read_csv("vectors/" + embedding_method + ".csv", header=None)
    if text == text:
        stripped = pre.strip_punctuation(text)
        tokens = pre.filter_stop_words_and_stem(stripped)
        if repr(stripped.strip()) == repr(''):
            return None
            # DON'T TAKE THE SENTENCE
        if len(word_tokenize(text)) < 4:
            return None
            # DON'T TAKE THE SENTENCE
    else:
        return None
    return tokens

def get_last_tweet_id():
    data = pd.read_csv("data_to_use.csv")
    last_tweet = data.iloc[0]
    last_tweet_id = last_tweet["tweet_id"]
    return last_tweet_id

def get_last_tweet_date():
    data = pd.read_csv("data_to_use.csv")
    last_tweet = data.iloc[0]
    last_tweet_date = last_tweet["date"]
    return last_tweet_date

def get_new_tweets_by_date(date):
    return fs.get_newcoming_tweets_since_date(date)

def get_new_tweets(last_tweet_id):
    last_tweet_snapshot = fs.get_tweet_snapshot_by_id(last_tweet_id)
    return fs.get_newcoming_tweets_since_document_by_snapshot(last_tweet_snapshot)

def is_new_group_needed(last_update_date, tweet_date):
    return tweet_date - last_update_date > news_group_lifetime

def get_newsgroup_id_for_news(cluster_id, newcomer_date):
    try:
        data = pd. read_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")
    except:
        return None
    ng_of_cls_id = data.where(data["cluster_id"] == cluster_id)
    ng_of_cls_id = ng_of_cls_id.dropna()
    if ng_of_cls_id.empty:
        return None
    ng_of_cls_id = ng_of_cls_id.sort_values(by=["created_at"], ascending=False)
    last_ng_of_cluster = ng_of_cls_id.iloc[0]
    if is_new_group_needed(last_ng_of_cluster["created_at"], newcomer_date):
        return None
    return last_ng_of_cluster["newsgroup_id"]

def create_cluster(tweet_id):
    cluster_id = uuid.uuid1()
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None)
    new_cluster = pd.DataFrame([{0:cluster_id, 1:tweet_id}], index=[0])
    cluster_data = cluster_data.append(new_cluster)
    cluster_data = cluster_data.reset_index(drop=True)
    cluster_data.to_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header = False, index=False)
    return cluster_id

def create_newsgroup(cluster_id, tweet_date, tweet_username):
    newsgroup_id = uuid.uuid1()
    new_newsgroup_local = {
        "newsgroup_id": newsgroup_id,
        "cluster_id": cluster_id,
        "created_at": tweet_date
    }
    new_newsgroup_local = pd.DataFrame(new_newsgroup_local, index=[0])
    # print(new_newsgroup_local)
    try:
        data = pd. read_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")
        data = data.append(new_newsgroup_local, ignore_index=True)
        data.reset_index(drop=True)
    except:
        data = new_newsgroup_local
    data.to_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", index=False)

    # -------
    return newsgroup_id

def assign_news_to_cluster(cluster_id, tweet_id):
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None)
    new_cluster = pd.DataFrame([[cluster_id, tweet_id]])
    cluster_data = cluster_data.append(new_cluster, ignore_index=True)
    cluster_data.to_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=False, index=False)


def update_database(tweet_id, newsgroup_id, create_newsgroup_firestore):
    fs.update_for_newcomer(tweet_id, newsgroup_id, create_newsgroup_firestore)

def save_newcomer_to_local(newcomer, text):
    data = pd.read_csv("data_to_use.csv", index_col=0)
    newcomer_df = pd.DataFrame([newcomer])
    new_data = newcomer_df.append(data, ignore_index=True)
    new_data = new_data.reset_index(drop=True)
    new_data.to_csv("data_to_use.csv")

    # data = pd.read_csv("tweets.csv", index_col=0)
    # newcomer_df = pd.DataFrame([newcomer])
    # new_data = newcomer_df.append(data, ignore_index=True)
    # new_data = new_data.reset_index(drop=True)
    # new_data.to_csv("tweets.csv")

    texts = pd.read_csv("texts.csv", header=None)
    new_text = pd.DataFrame([[newcomer["tweet_id"],text]])
    new_text_df = new_text.append(texts, ignore_index=True)
    # new_text_df = new_text_df.reset_index(drop=True)
    new_text_df.to_csv("texts.csv", header=False, index=False)


def main():
    print("Started Checking...")
    # last_tweet_id = get_last_tweet_id()
    # newcoming_news = get_new_tweets(last_tweet_id)
    last_tweet_date = get_last_tweet_date()
    newcoming_snapshots = get_new_tweets_by_date(last_tweet_date)
    newcoming_news = []
    for snapshot in newcoming_snapshots:
        snapshot_dict = snapshot.to_dict()
        snapshot_dict["document_reference"] = snapshot.reference
        newcoming_news.append(snapshot_dict)
    print(str(len(newcoming_news)), "Newcoming news were found")
    for newcomer in newcoming_news:
        print()
        print("Newcomer Tweet ID:", newcomer["tweet_id"])
        print("By:", newcomer["username"])
        # if newcomer["tweet_id"] == last_tweet_id:
        #     continue
        create_newsgroup_firestore = False
        preprocessed = preprocess(newcomer["text"])
        if preprocessed is None:
            print("Bad text!")
            continue
        cluster_id = incrementor.perform2(embedding_method, linkge_method, d_metric, d_threshod, inc_d_threshold, multiplier, newcomer["text"], newcomer["tweet_id"])
        if cluster_id is None:
            print("Creating new cluster...")
            new_cluster_id = create_cluster(newcomer["tweet_id"])
            newsgroup_id = create_newsgroup(new_cluster_id, newcomer["date"], newcomer["username"])
            create_newsgroup_firestore = True
            print("New cluster and news group are created!")
        else:
            print("Cluster found!")
            assign_news_to_cluster(cluster_id, newcomer["tweet_id"])
            newsgroup_id = get_newsgroup_id_for_news(cluster_id, newcomer["date"])
            if newsgroup_id is None:
                print("Creating new news group...")
                newsgroup_id = create_newsgroup(cluster_id, newcomer["date"], newcomer["username"])
                create_newsgroup_firestore = True
                print("New news group is created!")
            else:
                print("Newsgroup found!")
        update_database(newcomer, newsgroup_id, create_newsgroup_firestore)
        print("Database is updated!")
        save_newcomer_to_local(newcomer, preprocessed)
        print("Local data is updated!")
        time.sleep(delay)
    print("Finished Checking!\n")

while True:
    main()
    time.sleep(check_freq)





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