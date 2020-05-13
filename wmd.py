import pandas as pd
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import KeyedVectors
import numpy as np
from scipy.spatial.distance import squareform
import scipy.cluster.hierarchy
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import cosine


def dist(model, set, type, model_type):
    distances = np.zeros((len(texts),len(texts)))
    for i in range(len(set)-1):
        print("At title:", str(i+1), "/", str(len(set)))
        for j in range(i+1, len(set)):
            # print("Calculating distances netween pairs:", i+1, "-", j+1)
            if model_type == "word2vec":
                if type == "wmd":
                    d = model.wv.wmdistance(word_tokenize(texts[i]), word_tokenize(texts[j]))
                else:
                    d = model.wv.similarity(word_tokenize(texts[i]), word_tokenize(texts[j]))
            else:
                # d = model.docvecs.similarity(model.infer_vector(word_tokenize(texts[i])), model.infer_vector(word_tokenize(texts[j])))
                # d = model.docvecs.similarity(str(i), str(j))
                vec1 = model.infer_vector(word_tokenize(texts[i]))
                vec2 = model.infer_vector(word_tokenize(texts[j]))
                d = cosine(vec1, vec2)

            distances[i][j] = abs(d)
            distances[j][i] = abs(d)
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
    for i in methods:
        try:
            links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances)
            df = pd.DataFrame(links)
            df.to_csv("linkages/" + title + "_" + i + ".csv", index=False, header=False)
            print("Linkage for", title, "with method", i, "was saved")
        except:
            print("Linkage for", title, "with method", i, "couldnt' be saved")


data = pd.read_csv("data_to_use.csv")
texts = pd.read_csv("texts.csv", header=None).to_numpy(dtype="str").T[1]


# title = "doc2vec_self_cosine"
# print("Started", title)
# tagged_docs = []
# for i in range(texts.shape[0]):
#     tagged_docs.append(TaggedDocument(words=word_tokenize(texts[i]), tags=[str(i)]))
# # print(texts[0].split())
# # documents = [TaggedDocument(doc.split(), [str(i)]) for i, doc in enumerate(texts)]
# model = Doc2Vec(min_count=1)
# model.build_vocab(tagged_docs)
# model.train(tagged_docs, epochs=model.epochs, total_examples=model.corpus_count)
# # model = Doc2Vec(documents)
# # model.init_sims(replace=False)
# distances = dist(model, texts, "cosine", "doc2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")

tokens = []
for i in range(texts.shape[0]):
    tokens.append(word_tokenize(texts[i]))
# title = "word2vec_self_cosine"
# print("Started", title)
# model = Word2Vec(tokens)
# # model.init_sims(replace=True)
# distances = dist(model, texts, "cosine", "word2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")
#
# title = "word2vec_google_news_cosine"
# print("Started", title)
# model = Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
# model.init_sims(replace=True)
# distances = dist(model, texts, "cosine", "word2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")
#
# title = "word2vec_combined_cosine"
# print("Started", title)
# model = Word2Vec(texts)
# model.init_sims(replace=True)
# model.intersect_word2vec_format('GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)
# model.train(texts)
# distances = dist(model, texts, "cosine", "word2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")

title = "word2vec_self_wmd"
print("Started", title)
model = Word2Vec(tokens)
model.init_sims(replace=True)
distances = dist(model, texts, "wmd", "word2vec")
df = pd.DataFrame(distances)
df.to_csv("distances/" + title + ".csv", index=False, header=False)
create_links(distances, title)
print("Finished", title, "\n")
#
# title = "word2vec_google_news_wmd"
# print("Started", title)
# model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
# model.init_sims(replace=True)
# distances = dist(model, texts, "wmd", "word2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")

# title = "word2vec_combined_wmd"
# print("Started", title)
# model = Word2Vec(tokens)
# model.init_sims(replace=True)
# model.intersect_word2vec_format('GoogleNews-vectors-negative300.bin.gz', lockf=1.0, binary=True)
# model.train(texts)
# distances = dist(model, texts, "wmd", "word2vec")
# df = pd.DataFrame(distances)
# df.to_csv("distances/" + title + ".csv", index=False, header=False)
# create_links(distances, title)
# print("Finished", title, "\n")
































# model1 = Word2Vec(texts)
# model1.init_sims(replace=True)
# print("Model1 created")
# distances1 = dist(model1, texts, "wmd")
# df = pd.DataFrame(distances1)
# df.to_csv("distances/wmd_self_train.csv", index=False, header=False)
# distances1 = squareform(distances1)
# print("Distances1 created")
#
# for i in methods:
#     links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances1)
#     df = pd.DataFrame(links)
#     df.to_csv("linkages/wmd_self_train_" + i + ".csv", index=False, header=False)
#     print("Linkage for self train with method", i, "was saved")
#
#
# model2 = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)
# model2.init_sims(replace=True)
# print("Model2 created")
# distances2 = wmd(model2, texts)
# df = pd.DataFrame(distances2)
# df.to_csv("distances/wmd_google_news.csv", index=False, header=False)
# distances2 = squareform(distances2)
# print("Distances2 created")
#
# for i in methods:
#     links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances2)
#     df = pd.DataFrame(links)
#     df.to_csv("linkages/wmd_google_news_" + i + ".csv", index=False, header=False)
#     print("Linkage for google news with method", i, "was saved")