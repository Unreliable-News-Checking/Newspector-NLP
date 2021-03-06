import pandas as pd
from scipy.cluster.hierarchy import fcluster
import numpy as np
import uuid

def clustering(code, threshold):
    data = pd.read_csv("data_to_use.csv")
    links = pd.read_csv("linkages/"+code+".csv", header=None).to_numpy()
    clusters = fcluster(links, criterion="distance", t=threshold)
    # texts = pd.read_csv("original_texts.csv", header=None).to_numpy()
    texts= data["text"]
    # texts = pd.read_csv("texts.csv", header=None).to_numpy()
    min = np.min(clusters)
    max = np.max(clusters)
    print(max)
    representation = ""
    # relation = {}
    relation = []
    for i in range(min, max+1):
        representation += "-----------------CLUSTER" + str(i) + "-----------------\n"
        cls = texts.iloc[np.where(clusters==i)]
        # print(cls.shape)
        for text in cls:
            representation += "-------ARTICLE-------\n" + text + "\n"
        representation += "\n"
        cluster_id = uuid.uuid1()
        # print(np.where(clusters==i))
        for k in np.where(clusters==i)[0]:
            print(k)
        # relation[uuid.uuid1()] = data.loc[np.where(clusters==i)]["tweet_id"]
            relation.append([cluster_id, data.loc[k]["tweet_id"]])

    text_file = open("cluster_representations/" + code + "_" + str(threshold) + ".txt", "w+", encoding="utf-8")
    n = text_file.write(representation)
    text_file.close()
    df = pd.DataFrame(relation)
    df.to_csv("clusters/" + code + "_" + str(threshold) + ".csv", header = False, index=False)


# clustering("tfidf_weighted_cosine", 0.9)
# clustering("tfidf_weighted_cosine", 0.85)
# clustering("roberta_cosine_weighted", 0.002)
# clustering("roberta_euclidean_ward", 1)
# clustering("roberta_tfidf_euclidean_ward", 1.75)
clustering("roberta_tfidf_ward_euclidean", 5)
# clustering("tfidf_weighted_jaccard", 0.85)
# clustering("tfidf_weighted_cosine", 0.8)
# clustering("bow_weighted_cosine", 0.9)
# clustering("bow_average_cosine", 0.85)
# clustering("bow_average_jaccard", 0.9)
# clustering("bow_single_cosine", 0.5)
# clustering("wmd_google_news_complete", 0.3)
# clustering("wmd_google_news_weighted", 0.25)
# clustering("wmd_self_train_weighted", 0.1)
# clustering("wmd_self_train_ward", 0.2)
# clustering("tfdif_single_cosine", 0.8)
# clustering("tfdif_weighted_dice", 0.8)
# clustering("doc2vec_self_cosine_complete", 0.8)
# clustering("doc2vec_self_cosine_weighted", 0.7)