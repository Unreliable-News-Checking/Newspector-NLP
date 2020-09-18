import os
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

folder = os.fsencode("linkages")
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    # if filename[:6] != "tfidf_" and filename[:4] != "bow_":
    if filename[:7] != "roberta":
        continue
    print("Computing dendrogram of", filename)
    links = pd.read_csv("linkages/" + filename, header=None)
    try:
        plt.figure(figsize=(10, 7))
        dendrogram(links,
                    orientation='top',
                    # labels=labelList,
                    distance_sort='descending',
                    show_leaf_counts=True)
        plt.savefig("dendrograms/" + filename.replace("csv", "png"))
    except:
        print("Couldn't compute", filename)