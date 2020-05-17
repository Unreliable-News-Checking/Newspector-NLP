import pandas as pd
import re
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer

def filter_stop_words_and_stem(sentence):
    ss = SnowballStemmer("english")
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
