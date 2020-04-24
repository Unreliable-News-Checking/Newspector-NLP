import sys
import pandas as pd
import numpy as np

def a():
    print(5)
getattr(sys.modules[__name__], "a")()


df = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
b = [0,2]
print(df.loc[b])

f = np.array([1,2,3])+5
print(f)