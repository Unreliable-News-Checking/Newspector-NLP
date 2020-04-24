from libs.gsdmm import MovieGroupProcess
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize

def create_vocabulary(text):
    tokens = word_tokenize(text)
    vocab = []
    for t in tokens:
        if t not in vocab:
            vocab.append(t)
    return vocab

texts = pd.read_csv("texts.csv", header=None).to_numpy(dtype="str").T[0]
texts = texts[:200]
vocabs = []
for text in texts:
    vocabs.append(create_vocabulary(text))

v = set(x for vocab in vocabs for x in vocab)
n_terms = len(v)

mvp = MovieGroupProcess(K=1000)
clusters = mvp.fit(texts, n_terms)

o_texts = pd.read_csv("original_texts.csv", header=None).to_numpy().T[0]
o_texts = o_texts[:200]
min = np.min(clusters)
max = np.max(clusters)
print(max)
representation = ""
for i in range(min, max+1):
    representation += "-----------------CLUSTER" + str(i) + "-----------------\n"
    cls = o_texts[np.where(clusters==i)]
    for text in cls:
        representation += "-------ARTICLE-------\n" + text[0] + "\n"
    representation += "\n"

text_file = open("cluster_representations/sttm.txt", "w")
n = text_file.write(representation)
text_file.close()