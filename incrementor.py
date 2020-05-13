import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine





# print(cluster_data)

# def create_newsgroup(news, cluster_id):


def perform(embedding_method, linkge_method, d_metric, d_threshod, inc_d_threshold, multiplier, new_sentence, new_id):
    stop_words = set(stopwords.words('english'))
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None).to_numpy()
    vectors = None
    texts = pd.read_csv("texts.csv", header=None, index_col=0)
    if embedding_method == "tfidf":
            #DON'T TAKE THE SENTENCE
        # print(texts)
        # texts.loc[texts.shape[0]] = [new_id,tokens]
        texts.loc[new_id] = new_sentence
        # print(type(texts.index.values[0]))
        # print(texts)
        texts_np = texts.to_numpy(dtype="str").T[0]
        vectorizer = TfidfVectorizer(stop_words=stop_words, lowercase=True)
        vectors = vectorizer.fit_transform(texts_np)
        vectors = pd.DataFrame(vectors.toarray(), index=list(texts.index.values))
        # print(vectors)
    clusters = {}
    for row in cluster_data:
        if row[0] in clusters:
            clusters[row[0]].append(row[1])
        else:
            clusters[row[0]] = [row[1]]

    distance_dict = {}
    for id in clusters:
        length = len(clusters[id])
        n_selection = int(np.log(length)/np.log(3)) + 1
        # selected = np.random.choice(clusters[id], n_selection, replace=False)
        selected = clusters[id]
        selected_vectors = vectors.loc[selected].to_numpy()
        distances = np.zeros(n_selection)
        for v in range(n_selection):
            # distances[v] = pdist(np.array([selected_vectors[v], vectors.loc[new_id]]))
            distances[v] = cosine(selected_vectors[v], vectors.loc[new_id].to_numpy())
            # print(distances[v])
        mean_distance = np.mean(distances)
        distance_dict[id] = mean_distance

    min_d = min(distance_dict.values())
    if min_d < inc_d_threshold:
        cluster_of_min_d = [k for k, v in distance_dict.items() if v == min_d][0]
        # print(cluster_of_min_d)
        for c in clusters[cluster_of_min_d]:
            print("---------ARTICLE--------")
            print(texts.loc[c])
        print("---------ARTICLE--------")
        print(new_sentence)
        return cluster_of_min_d
    else:
        print("New cluster should be created")
        return None

# perform()