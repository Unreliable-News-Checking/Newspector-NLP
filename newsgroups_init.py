import uuid

import pandas as pd
from services import firestore_services
import numpy as np


embedding_method = "tfidf"
linkge_method = "weighted"
d_metric = "cosine"
d_threshod = 0.85
fs = firestore_services.FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")

def create_newsgroup(cluster_id, tweet_date, tweet_username):
    newsgroup_id = uuid.uuid1()
    new_newsgroup_local = {
        "newsgroup_id": newsgroup_id,
        "cluster_id": cluster_id,
        "created_at": tweet_date,
        "updated_at": tweet_date
    }
    new_newsgroup_local = pd.DataFrame(new_newsgroup_local, index=[0])
    # print(new_newsgroup_local)
    try:
        data = pd. read_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv")
        data = data.append(new_newsgroup_local, ignore_index=True)
    except:
        data =new_newsgroup_local
    data.to_csv("clusters_newsgroups/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", index=False)

    new_newsgroup_db = {
        "category": "",
        "category_map": {},
        "created_at": int(tweet_date),
        "group_leader": tweet_username,
        "is_active": True,
        "source_count_map": {},
        "updated_at": int(tweet_date)
        # ----------------------NEED TO BE FILLED--------------------------
    }
    return newsgroup_id, new_newsgroup_db

def update_database(tweet_id, newsgroup_id, newsgroup_data):
    fs.update_for_newcomer(tweet_id, newsgroup_id, newsgroup_data)


cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None).to_numpy()
data = pd.read_csv("data_to_use.csv")

clusters = {}
for row in cluster_data:
    if row[0] in clusters:
        clusters[row[0]].append(row[1])
    else:
        clusters[row[0]] = [row[1]]

earliest_tweet_ids = []
newsgroup_ids_wrt_clusters = []
count = 0
for cluster_id in clusters:
    print("Creating Newsgroups of cluster:", str(count), "/", str(len(clusters)))
    dates = []
    usernames = []
    for i, id in enumerate(clusters[cluster_id]):
        # print(i)
        tmp = data.where(data["tweet_id"] == id)[["date","username"]]
        tmp = tmp.dropna()
        # print(tmp["date"].iloc[0])
        dates.append(tmp["date"].iloc[0])
        usernames.append(tmp["username"].iloc[0])
    # print(dates)
    dates = np.array(dates)
    # print(dates)
    usernames = np.array(usernames)
    index_of_min_date = np.argmin(dates)
    # print(index_of_min_date)
    earliest_tweet_id = clusters[cluster_id][index_of_min_date]
    # print("earliest twewet id:", earliest_tweet_id)
    earliest_tweet_ids.append(earliest_tweet_id)
    #Aynı tweetten birden fazla var o yüzden [0] koydum
    min_date = dates[index_of_min_date]
    # print(min_date)
    # print()
    earliest_tweet_username = usernames[index_of_min_date]
    newsgroup_id, newsgroup_data = create_newsgroup(cluster_id, min_date, earliest_tweet_username)
    newsgroup_ids_wrt_clusters.append(newsgroup_id)
    update_database(earliest_tweet_id, newsgroup_id, newsgroup_data)
    # aaa = data["tweet_id"].where(data["date"].where(data["tweet_id"] == clusters[cluster_id]).min() == data["date"])
    count += 1

count = 0
for cluster_id in clusters:
    print("Assigning Newsgroups of cluster:", str(count), "/", str(len(clusters)))
    for i, id in enumerate(clusters[cluster_id]):
        if id == earliest_tweet_ids[count]:
            continue
        update_database(id, newsgroup_ids_wrt_clusters[count], None)
    count += 1