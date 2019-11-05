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
    appAndInstll={}
    df = data_set[['App Name','Installs']]
    df = df.set_index('App Name').T.to_dict('records')
    list_of_word_instl = []
    for k,v in df[0].items():
        instl = v.replace(',','')
        instl = instl.replace('+','')
        try:
            if(int(instl)):
                text = re.sub(r'[^\w\s]','',k)
                text = ([word.lower() for word in word_tokenize(text) if word not in stopWordsList])
                list_of_word_instl.extend(list(map(lambda x: (x,int(instl)), text))) #array of tuples with words and installations
                uniqueWords.extend(text)
        except:
            continue
        

    uniqueWords = set(uniqueWords)
    for i in uniqueWords:
        num = list(map(lambda x: x[1],list(filter(lambda x: x[0]==i, list_of_word_instl)))) #[('food',10000),('foods',12000)] #'food':[1,2,4]
        print(i,np.mean(num)) #word wrt to installation mean

def textMining():
    data_set = loadData()
    cleanData(data_set)