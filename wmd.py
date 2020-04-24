import pandas as pd
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
from scipy.spatial.distance import squareform
import scipy.cluster.hierarchy

def filter_stop_words(sentence):
    stop_words = set(stopwords.words('english'))
    stop_words.add("s")
    stop_words.add("news")
    stop_words.add("live")
    stop_words.add("follow")
    word_tokens = word_tokenize(sentence)

    return [w for w in word_tokens if w not in stop_words or w[0] != "@"]


def strip_punctuation(sentence):
    return re.sub(r'[^\w\s]', '', sentence)


stop_words = set(stopwords.words('english'))

data = pd.read_csv("tweets.csv")
texts = []
data = data[-2000:]
for index, row in data.iterrows():
    text = row["text"]
    # print(row["time"])
    if text == text:
        stripped = strip_punctuation(text)
        if repr(stripped.strip()) == repr(''):
            data = data.drop(index, axis=0)
            continue
        texts.append(stripped)
    else:
        data = data.drop(index, axis=0)

def wmd(model, set):
    distances = np.zeros((len(texts),len(texts)))
    for i in range(len(set)-1):
        print("At index:", i)
        for j in range(i+1, len(set)):
            # print("Calculating distances netween pairs:", i+1, "-", j+1)
            d = model.wv.wmdistance(texts[i], texts[j])
            distances[i][j] = d
            distances[j][i] = d
            # print("Calculated distance:", distances[i][j])
            # print("Between:")
            # print("-----------Article--------")
            # print(texts[i])
            # print("-----------Article--------")
            # print(texts[j])

    return distances

model1 = Word2Vec(texts)
model1.init_sims(replace=True)
print(model1.wv.shape)
print("Model1 created")
distances1 = wmd(model1, texts)
df = pd.DataFrame(distances1)
df.to_csv("distances/wmd_self_train", index=False, header=False)
distances1 = squareform(distances1)
print("Distances1 created")

model2 = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
model2.init_sims(replace=True)
print("Model2 created")
distances2 = wmd(model2, texts)
df = pd.DataFrame(distances2)
df.to_csv("distances/wmd_google_news", index=False, header=False)
distances2 = squareform(distances2)
print("Distances2 created")

methods = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
for i in methods:
    # links = getattr(scipy.cluster.hierarchy, 'f%d' % i)(distances1)
    # df = pd.DataFrame(links)
    # df.to_csv("linkages/wmd_self_train_" + i + ".csv", index=False, header=False)
    # print("Linkage for self train with method", i, "was saved")

    links = getattr(scipy.cluster.hierarchy, 'f%d' % i)(distances2)
    df = pd.DataFrame(links)
    df.to_csv("linkages/wmd_google_news_" + i + ".csv", index=False, header=False)
    print("Linkage for google news with method", i, "was saved")