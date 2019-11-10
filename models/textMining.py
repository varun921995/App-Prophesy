import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
import string
import re
import numpy as np
import json

def loadData():
    path_to_file = "dataset/Google-Playstore-32K.csv"
    data_set = pd.read_csv(path_to_file)
    return data_set

def cleanData(data_set):
    #unique words from all application names
    stopWordsList = stopwords.words("english")
    uniqueWords = []
    englishWords = words.words()

    df = data_set[['App Name','Installs','Category']]

    # df['Installs'] =  pd.to_numeric(df['Installs'].str.replace('[^\w\s]',''))
    df['Installs'] = pd.to_numeric(df['Installs'].str.replace('[^\w\s]',''),errors='ignore')
    df['App Name'] = (df['App Name'].str.replace('[^\w\s]',''))

    df_dict = {}

    for idx in range(df.shape[0]):
        try:
            if(int(df.loc[idx, 'Installs'])):
                text = [word.lower() for word in word_tokenize(df.loc[idx, 'App Name']) if (word not in stopWordsList and word in englishWords)]
                z = [ (a,int(df.loc[idx, 'Installs'])) for a in text ]
                df_dict.setdefault(df.loc[idx, 'Category'],[]).extend(list(filter(lambda x: x[0] not in stopWordsList, z)))
                uniqueWords.extend(text)
        except:
            continue
    uniqueWords = set(uniqueWords)
    return uniqueWords,df_dict

def mapWordsWithInstll(uniqueWords,df_dict):
    a={}
    for k,v in df_dict.items():
        a = [(uk,sum([vv for kk,vv in v if kk==uk])/len([vv for kk,vv in v if kk==uk])) for uk in uniqueWords if (len(uk)>1) if ( sum([vv for kk,vv in v if kk==uk])!= 0)]
        df_dict[k] = dict(a)
    return df_dict
    
# For value without category    
#     num = []
#     b={}
#     for j in uniqueWords:
#         num = list(map(lambda x: x[1],list(filter(lambda x: x[0]==j, v)))) #[('food',10000),('foods',12000)] #'food':[1,2,4]
#         if(len(num)!=0):
# #             print(j,np.mean(num))
#             b[j]=np.mean(num)
#     df_dict[k] = b
# #             df_dict[k] = (j,np.mean(num))

def storeJson(jsonData):
    with open('dataset/dataWithWords.json', 'w') as outfile:
        json.dump(jsonData, outfile)

def textMining():
    data_set = loadData()
    uniqueWords,df_dict = cleanData(data_set)
    jsonForm = mapWordsWithInstll(uniqueWords,df_dict)
    storeJson(jsonForm)