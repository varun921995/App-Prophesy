import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re


def loadData():
    path_to_file = "dataset/Google-Playstore-32K.csv"
    data_set = pd.read_csv(path_to_file)
    return data_set

def cleanData(data_set):
    #unique words from all application names
    stopWordsList = stopwords.words("english")
    uniqueWords = []
    for name in data_set['App Name']:
        text = re.sub(r'[^\w\s]','',name)
        text = ([word.lower() for word in word_tokenize(text) if word not in stopWordsList])
        uniqueWords.extend(text)

    uniqueWords = set(uniqueWords)
    print(uniqueWords)

def textMining():
    data_set = loadData()
    cleanData(data_set)