import pandas as pd
from scipy.cluster.hierarchy import fcluster
import numpy as np
import uuid

def clustering(code, threshold):
    data = pd.read_csv("data_to_use.csv")
    links = pd.read_csv("linkages/"+code+".csv", header=None).to_numpy()
    clusters = fcluster(links, criterion="distance", t=threshold)
    texts = pd.read_csv("original_texts.csv", header=None).to_numpy()
    # texts = pd.read_csv("texts.csv", header=None).to_numpy()
    min = np.min(clusters)
    max = np.max(clusters)
    print(max)
    representation = ""
    relation = {}
    for i in range(min, max+1):
        representation += "-----------------CLUSTER" + str(i) + "-----------------\n"
        cls = texts[np.where(clusters==i)]
        for text in cls:
            representation += "-------ARTICLE-------\n" + text[0] + "\n"
        representation += "\n"
        relation[uuid.uuid1()] = data.loc[np.where(clusters==i)+5615]["tweet_id"]

    text_file = open("cluster_representations/" + code + "_" + str(threshold) + ".txt", "w+", encoding="utf-8")
    n = text_file.write(representation)
    text_file.close()
    df = pd.DataFrame(relation)
    df.to_csv("clusters/" + code + "_" + str(threshold) + ".txt")


clustering("tfdif_weighted_cosine", 0.8)
# clustering("tfdif_single_cosine", 0.8)
# clustering("tfdif_weighted_dice", 0.8)