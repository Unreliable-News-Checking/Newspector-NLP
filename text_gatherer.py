import pandas as pd
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from services import preprocessing as pre

n_data = 2000
# ps = PorterStemmer()


stop_words = set(stopwords.words('english'))

data = pd.read_csv("tweets.csv")
data = data[:200]
texts = []
# data = data[-n_data:]
original_texts = []
# print(data.iloc[-1])
for index, row in data.iterrows():
    text = row["text"]
    # print(row["date"])
    if text == text:
        stripped = pre.strip_punctuation(text)
        tokens = pre.filter_stop_words_and_stem(stripped)
        if repr(stripped.strip()) == repr(''):
            print(row["tweet_id"])
            print(row["username"])
            print()
            data = data.drop(index, axis=0)
            continue
        texts.append(tokens)
        original_texts.append(text)
    else:
        print(row["tweet_id"])
        print(row["username"])
        print()
        data = data.drop(index, axis=0)

# data = data.drop(["news_group_id"], axis = 1)
data = data.reset_index(drop=True)
print(data.shape)
df = pd.DataFrame(texts, index=data.loc[:]["tweet_id"].to_list())
df.to_csv("texts.csv", header=False)
df = pd.DataFrame(original_texts)
df.to_csv("original_texts.csv", header=False, index=False)

df = pd.DataFrame(data)
df.to_csv("data_to_use.csv", index = False)