import sys
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist

def a():
    print(5)
getattr(sys.modules[__name__], "a")()


df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
b = [0,2]
print(df.loc[b])

f = np.array([1,2,3])+5
print(f)

# data = pd.read_csv("data_to_use.csv")
# print(len(data.loc[:]["tweet_id"].to_list()))

print(int(np.log(9)/np.log(3)))
print(np.zeros(3))

X = np.array([[6,8],[3,4]])
print(pdist(X, "euclidean"))
texts = pd.read_csv("texts.csv", header=None)
print(texts)