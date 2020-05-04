import pandas as pd
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer

n_data = 2000
# ps = PorterStemmer()
ss = SnowballStemmer("english")

def filter_stop_words_and_stem(sentence):
    stop_words = set(stopwords.words('english'))
    stop_words.add("s")
    stop_words.add("news")
    stop_words.add("live")
    stop_words.add("follow")
    word_tokens = word_tokenize(sentence)



    tokens = [ss.stem(w) for w in word_tokens if w not in stop_words and w[0] != "@"]
    sent = ""
    for t in tokens:
        sent += t + " "

    return sent[:len(sent)-1].lower()

def strip_punctuation(sentence):
    return re.sub(r'[^\w\s]', '', sentence)


stop_words = set(stopwords.words('english'))

data = pd.read_csv("tweets.csv")
texts = []
# data = data[-n_data:]
original_texts = []
# print(data.iloc[-1])
for index, row in data.iterrows():
    text = row["text"]
    # print(row["date"])
    if text == text:
        stripped = strip_punctuation(text)
        tokens = filter_stop_words_and_stem(stripped)
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

data = data.reset_index(drop=True)
print(data.shape)
df = pd.DataFrame(texts, index=data.loc[:]["tweet_id"].to_list())
df.to_csv("texts.csv", header=False)

df = pd.DataFrame(original_texts)
df.to_csv("original_texts.csv", header=False, index=False)

df = pd.DataFrame(data)
df.to_csv("data_to_use.csv", index = False)