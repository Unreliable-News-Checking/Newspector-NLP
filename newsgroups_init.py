import pandas as pd


embedding_method = "tfidf"
linkge_method = "weighted"
d_metric = "cosine"
d_threshod = 0.85

cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None).to_numpy()

clusters = {}
for row in cluster_data:
    if row[0] in clusters:
        clusters[row[0]].append(row[1])
    else:
        clusters[row[0]] = [row[1]]
