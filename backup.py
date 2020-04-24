# linked = linkage(vectors, 'ward')
# print(linked)
# labelList = range(1, 11)
#
# plt.figure(figsize=(10, 7))
# dendrogram(linked,
#             orientation='top',
#             # labels=labelList,
#             distance_sort='descending',
#             show_leaf_counts=True)
# plt.show()
#
# cls = AgglomerativeClustering(distance_threshold=1.5, n_clusters=None).fit(vectors)
# plt.figure()
# plt.scatter(vectors[:,0], vectors[:,1], c=cls.labels_, cmap='rainbow')
# plt.show()
# print("Cluster Amount:", cls.n_clusters_)
# for i in cls.labels_:
#     print(i, end=", ")
# print()
# for i in range(cls.labels_.shape[0]):
#     if cls.labels_[i] == 0:
#         print("--------ARTICLE-------")
#         print(texts[i])
