import pandas as pd
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from scipy.spatial.distance import pdist

def compute_linkages(X, method, metric):
    links = linkage(X, method=method, metric=metric)
    df = pd.DataFrame(links)
    df.to_csv("linkages/tfidf_" + method + "_" + metric + ".csv", index=False, header=False)

stop_words = set(stopwords.words('english'))

data = pd.read_csv("data_to_use.csv")
texts = pd.read_csv("texts.csv", header=None).to_numpy(dtype="str").T[1]
vectorizer = TfidfVectorizer(stop_words=stop_words, lowercase=True)
vectors = vectorizer.fit_transform(texts)
df_vecs = pd.DataFrame(vectors.toarray(), index=data.loc[:]["tweet_id"].to_list())
df_vecs.to_csv("vectors/tfidf.csv", header=False)
print(vectors.shape)
vecs = np.array(vectors.toarray())
for i, row in enumerate(vecs):
    if np.sum(row == 0) == row.shape[0]:
        # print(data.loc[i+5661, ["text", "tweet_id"]])
        # print(repr(data.loc[i + 5661, "text"]))
        print(repr(texts[i].strip()) == repr('\xa0'))
        print(repr(texts[i].strip()) == repr(''))
# a = np.array([[0,0,0],[1,2,3]])
# print(np.sum(a[0] == 0))
# print(a[0].shape)

# methods = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
# methods = ["single", "complete", "average", "weighted"]
# metrics = ["cosine", "jaccard", "dice"]
methods = ["weighted"]
metrics = ["cosine"]
for i in methods:
    for j in metrics:
        print("For", i, "method and", j, "metric")
        compute_linkages(vecs, i, j)

