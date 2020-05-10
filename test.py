import sys
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist

def a():
    print(5)
getattr(sys.modules[__name__], "a")()

#
# df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
# b = [0,2]
# print(df.loc[b])
#
# f = np.array([1,2,3])+5
# print(f)
#
# # data = pd.read_csv("data_to_use.csv")
# # print(len(data.loc[:]["tweet_id"].to_list()))
#
# print(int(np.log(9)/np.log(3)))
# print(np.zeros(3))
#
# X = np.array([[6,8],[3,4]])
# print(pdist(X, "euclidean"))
# texts = pd.read_csv("texts.csv", header=None)
# print(texts)

import time, threading
# def foo():
#     print(time.ctime())
#     threading.Timer(1, foo).start()
#     for i in range(100000000):
#         a=1
#     print(i)
#
# foo()

# def foo():
#     print(time.ctime())
#     for i in range(100000000):
#         a = 1
#     print(i)
#
# while True:
#     foo()
#     time.sleep(1)

# from datetime import datetime
#
# # dt_object = datetime.now()
# #
# # print(dt_object.replace(hour=0, minute=0, second=0, microsecond=0))
# dt1 = datetime.now()
# # time.sleep(1)
# # dt2 = datetime.now()
# dt2 = "2020-05-03 22:43:44.868052"
# print(dt1)
# # print(dt2)
# print(dt2 < str(dt1))
# # print("type(dt_object) =", type(dt_object))
#
# cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#         'Price': [22000,25000,27000,35000]
#         }
#
# df = pd.DataFrame(cars)
# df = df.where(df["Price"] == 25000)
# df = df.dropna(thresh=1)
# print(df)

# embedding_method = "tfidf"
# linkge_method = "weighted"
# d_metric = "cosine"
# d_threshod = 0.85
# #
# cluster_data = pd.read_csv("clusters/" + embedding_method + "_" + linkge_method + "_" + d_metric + "_" + str(d_threshod) + ".csv", header=None).to_numpy()
# data = pd.read_csv("data_to_use.csv")
#
# clusters = {}
# for row in cluster_data:
#     if row[0] in clusters:
#         clusters[row[0]].append(row[1])
#     else:
#         clusters[row[0]] = [row[1]]
#
# lst = []
# for cluster_id in clusters:
#     min_date = None
#     id_of_min_date = None
#     for i, id in enumerate(clusters[cluster_id]):
#         # print(str(i))
#         date = data.where(data["tweet_id"] == id)[["date", "username"]]
#         date = date.dropna()
#         print(date)
#         # print(min_date)
#         # if i == 0 or date.item() < min_date:
#         #     min_date = date.item()
#         #     id_of_min_date = id
#     lst.append(min_date)
    # lst.append(data["date"].where(data["tweet_id"] == clusters[cluster_id]).min())
    # lst.append(data["tweet_id"].where(data["date"].where(data["tweet_id"] == clusters[cluster_id]).min() == data["date"]))
# print(len(lst))
# print(len(clusters))

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import pandas as pd
# from datetime import datetime
#
# class FireStoreServices(object):
#
#     def __init__(self, credentials_resource):
#         self.cred = credentials.Certificate(credentials_resource)
#         self.app = firebase_admin.initialize_app(self.cred)
#         self.db = firestore.client()
#
# fss = FireStoreServices("newspector-backend-firebase-adminsdk-ws3xc-bd1c31a298.json")
# dic = fss.db.collection(u'tweets').document(u"1k5CFgcHTOKnLfyGEwVf").get().to_dict()
# tms = int(dic["retweet_date"][0] / 1000)
# print(tms)
# dt_object = datetime.fromtimestamp(tms)
# print(dt_object)
#
# df = pd.DataFrame(dic)
# df.to_csv("a.csv")


# data = pd.read_csv("data_to_use.csv")
# # print(type(int(data["date"].iloc[0])))
# # data = data.where(data["tweet_id"] == 1)
# # data = data.dropna()
# # print(data.empty)
# lst = data.to_list()

# texts = pd.read_csv("texts.csv", header=None)
# print(texts)
# new_text = pd.DataFrame([[123,"abc"]])
# print(new_text)
# ccc = new_text.append(texts, ignore_index=True)
# ccc = ccc.reset_index(drop=True)
# print(ccc)
# a = [1,2,3]
# ad = pd.DataFrame(a)
# print(ad.loc[[5]])
texts = pd.read_csv("texts.csv", header=None, index_col=0)
data = pd.read_csv("data_to_use.csv", index_col=0)
print(texts)
print(texts.shape)
print(data.shape)
print(texts.iloc[106][1])
texts2 = texts[131:]
print(texts2.iloc[0][1])

# print(data)
data2 = data[131:]
data2 = data2.reset_index(drop=True)
# print(data2)
print(data2["text"].iloc[0])
print(data2.shape)
texts2.to_csv("texts.csv", header=False)
data2.to_csv("data_to_use.csv")






# # print(cluster_data.shape)
# from scipy.spatial.distance import squareform
# import scipy.cluster.hierarchy
# distances1 = pd.read_csv("distances/wmd_self_train.csv", header=None).to_numpy()
# distances1 = squareform(distances1)
# distances2 = pd.read_csv("distances/wmd_google_news.csv", header=None).to_numpy()
# distances2 = squareform(distances2)
#
#
# methods = ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
# for i in methods:
#     links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances1)
#     df = pd.DataFrame(links)
#     df.to_csv("linkages/wmd_self_train_" + i + ".csv", index=False, header=False)
#     print("Linkage for self train with method", i, "was saved")
#
#     links = getattr(scipy.cluster.hierarchy, '%s' % i)(distances2)
#     df = pd.DataFrame(links)
#     df.to_csv("linkages/wmd_google_news_" + i + ".csv", index=False, header=False)
#     print("Linkage for google news with method", i, "was saved")