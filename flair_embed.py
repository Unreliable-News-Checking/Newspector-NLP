import pandas as pd

from flair.embeddings import TransformerDocumentEmbeddings, DocumentPoolEmbeddings, DocumentRNNEmbeddings
from flair.data import Sentence
from scipy.spatial.distance import cosine, euclidean
import scipy.cluster.hierarchy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

import numpy as np
from scipy.spatial.distance import squareform


def dist(vectors, texts):
    distances = np.zeros((len(texts), len(texts)))
    for i in range(len(texts) - 1):
        print("At title:", str(i + 1), "/", str(len(texts)))
        for j in range(i + 1, len(texts)):
            #             print(vectors[i])
            #             print(vectors[j])
            #             d = cosine(vectors[i], vectors[j])
            d = euclidean(vectors[i], vectors[j])
            distances[i][j] = d
            distances[j][i] = d
            # print("Calculated distance:", distances[i][j])
            # print("Between:")
            # print("-----------Article--------")
            # print(texts[i])
            # print("-----------Article--------")
            # print(texts[j])
    print(distances.shape)
    return distances


def create_links(distances, title):
    # methods = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
    methods = ["single", "complete", "average", "weighted"]
    distances = squareform(distances)
    links = scipy.cluster.hierarchy.ward(distances)
    df = pd.DataFrame(links)
    df.to_csv("C:/Users/kaang/Desktop/news_clustering/clustering/linkages/roberta_tfidf_ward_euclidean.csv",
              index=False, header=False)


#     for i in methods:
#         try:
#             links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances)
#             df = pd.DataFrame(links)
#             df.to_csv("C:/Users/kaang/Desktop/news_clustering/clustering/linkages/" + title + "_" + i + ".csv", index=False, header=False)
#             print("Linkage for", title, "with method", i, "was saved")
#         except:
#             print("Linkage for", title, "with method", i, "couldnt' be saved")
#         links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances)
#         links = scipy.cluster.hierarchy.ward(distances)
#         df = pd.DataFrame(links)
#         df.to_csv("C:/Users/kaang/Desktop/news_clustering/clustering/linkages/" + title + "_" + i + ".csv", index=False, header=False)
#         print("Linkage for", title, "with method", i, "was saved")


data = pd.read_csv("C:/Users/kaang/Desktop/news_clustering/clustering/data_to_use.csv")
texts = pd.read_csv("C:/Users/kaang/Desktop/news_clustering/clustering/texts.csv", header=None).to_numpy(dtype="str").T[
    1]
# texts = pd.read_csv("C:/Users/kaang/Desktop/news_clustering/clustering/original_texts.csv", header=None).to_numpy(dtype="str").T[0]
title = "roberta_cosine"

# %%

transformer_embeddings = TransformerDocumentEmbeddings('roberta-base')

# %%

vectorizer = TfidfVectorizer(lowercase=True)
tfidf_vectors = vectorizer.fit_transform(texts)
tfidf_vectors = tfidf_vectors.toarray()

# %%

vectors = []
for text in texts:
    sentence = Sentence(text)
    transformer_embeddings.embed(sentence)
    vec = sentence.embedding.detach().numpy()
    vectors.append(vec)
vectors = np.concatenate((vectors, tfidf_vectors), axis=1)
vectors = normalize(vectors, axis=0)

distances = dist(vectors, texts)

# %%

create_links(distances, title)