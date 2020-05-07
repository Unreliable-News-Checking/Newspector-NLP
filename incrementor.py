import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
import text_gatherer as tg
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine




# print(cluster_data)

# def create_newsgroup(news, cluster_id):


def perform(embedding_method, linkge_method, d_metric, d_threshod, multiplier, new_sentence, new_id):
    cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None).to_numpy()
    tokens = None
    vectors = None
    texts = pd.read_csv("texts.csv", header=None, index_col=0)
    if embedding_method == "tfidf":
        stop_words = set(stopwords.words('english'))
        # vectors = pd.read_csv("vectors/" + embedding_method + ".csv", header=None)
        if new_sentence == new_sentence:
            stripped = tg.strip_punctuation(new_sentence)
            tokens = tg.filter_stop_words_and_stem(stripped)
            if repr(stripped.strip()) == repr(''):
                return None
                # DON'T TAKE THE SENTENCE
        else:
            return None
            #DON'T TAKE THE SENTENCE
        # print(texts)
        # texts.loc[texts.shape[0]] = [new_id,tokens]
        texts.loc[new_id] = tokens
        # print(type(texts.index.values[0]))
        # print(texts)
        texts_np = texts.to_numpy(dtype="str").T[0]
        vectorizer = TfidfVectorizer(stop_words=stop_words, lowercase=True)
        vectors = vectorizer.fit_transform(texts_np)
        vectors = pd.DataFrame(vectors.toarray(), index=list(texts.index.values))
        print(vectors)
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
        selected = np.random.choice(clusters[id], n_selection, replace=False)
        selected_vectors = vectors.loc[selected].to_numpy()
        # selected_vectors = vectors.loc[selected.tolist()].to_numpy()
        # distances = cosine_similarity([vectors.loc[new_id].to_numpy()], selected_vectors)
        # print(distances)
        distances = np.zeros(n_selection)
        for v in range(n_selection):
            # distances[v] = pdist(np.array([selected_vectors[v], vectors.loc[new_id]]))
            distances[v] = cosine(selected_vectors[v], vectors.loc[new_id].to_numpy())
            # print(distances[v])
        mean_distance = np.mean(distances)
        distance_dict[id] = mean_distance

    min_d = min(distance_dict.values())
    if min_d < d_threshod:
        cluster_of_min_d = [k for k, v in distance_dict.items() if v == min_d][0]
        print(cluster_of_min_d)
        for c in clusters[cluster_of_min_d]:
            print("---------ARTICLE--------")
            print(texts.loc[c])
        print("---------ARTICLE--------")
        print(new_sentence)
        return cluster_of_min_d
    else:
        print("New cluster should be created")
        return -1

# perform()