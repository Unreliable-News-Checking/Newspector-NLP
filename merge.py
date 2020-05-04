import pandas as pd

df1 = pd.read_csv("tweets3.csv")
df2 = pd.read_csv("tweets2.csv")

df3 = df1.append(df2)
df3 = df3.sort_values(by=["date"], ascending=False)
df3.to_csv("tweets.csv")