# Author Gaganpreet Singh
# includes method for preprocessing of the data , which is further used to display trends, train models and predict.

import re
import sys

import time
import datetime

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import random
from flask import Blueprint
import joblib


def preProcessData():
    data = pd.read_csv('dataset/Google-Playstore-32K.csv', delimiter=',')
    data.dataframeName = 'Google-Playstore-32K.csv'

    data = data.sort_values('Installs', ascending=False)
    data = data.drop_duplicates(subset='App Name', keep='first')

    # detect null cols and null rate
    nulls = [i for i in data.isna().any().index if data.isna().any()[i] == True]
    rates = []
    counts = []
    for i in nulls:
        rates.append((data[i].isna().sum()/data.shape[0])*100)
        counts.append(data[i].isna().sum())
    null_df = pd.DataFrame.from_dict(
        {"Col": nulls, "Count": counts, "Null_Rates": rates})
    null_df

    # delete Type,Content Rating, Current Ver, Android Ver null values row
    df_train = data.copy()
    for i in ['Reviews', 'Latest Version']:
        df_train = df_train.drop(df_train.loc[df_train[i].isnull()].index, 0)

    df_train['Rating'].replace('Lessons', np.nan, inplace=True)
    df_train['Rating'].replace('GAME_STRATEGY', np.nan, inplace=True)
    df_train['Rating'].replace('NEWS_AND_MAGAZINES', np.nan, inplace=True)
    df_train['Rating'] = df_train['Rating'].fillna(df_train['Rating'].median())

    # for i in ['Rating']:
    #     df_train = df_train.drop(df_train.loc[df_train[i].isnull()].index,0)
    df_train['Rating'].astype(float).describe()

    df_train['Installs'] = df_train['Installs'].apply(
        lambda x: x.strip('+').replace(',', ''))
    df_train.Installs.unique()

    regex = [r'GAME_[A-Za-z]+.*']
    for j in regex:
        df_train['Category'] = df_train['Category'].astype(
            str).apply(lambda x: re.sub(j, 'GAME', x))

    regex = [r'[-+|/:/;(_)@\[\]#�,>]', r'\s+', r'[A-Za-z]+']
    for j in regex:
        df_train['Latest Version'] = df_train['Latest Version'].astype(
            str).apply(lambda x: re.sub(j, '0', x))
    df_train['Latest Version'].replace('?.?', np.nan, inplace=True)

    df_train['Latest Version'] = df_train['Latest Version'].astype(str).apply(
        lambda x: x.replace('.', ',', 1).replace('.', '').replace(',', '.', 1)[:3]).astype(float)
    df_train['Latest Version'] = df_train['Latest Version'].fillna(
        df_train['Latest Version'].median())

    df_train['Category'].replace(' Channel 2 News', np.nan, inplace=True)
    df_train['Category'].replace(')', np.nan, inplace=True)
    df_train = df_train[pd.notnull(df_train['Category'])]

    le = preprocessing.LabelEncoder()
    df_train["AppName_LE"] = le.fit_transform(df_train["App Name"])

    # Category features encoding

    # Encode Content Rating features
    category = preprocessing.LabelEncoder()
    df_train['Category_LE'] = category.fit_transform(df_train['Category'])

    # Encode Content Rating features
    content = preprocessing.LabelEncoder()
    df_train['ContentRating_LE'] = content.fit_transform(
        df_train['Content Rating'])
    df_train['Price'] = df_train['Price'].apply(lambda x: x.strip('$'))

    df_train['Price'].replace('Varies with device', np.nan, inplace=True)
    df_train['Price'] = df_train['Price'].fillna(df_train['Price'].median())

    df_train['Type'] = np.where(
        df_train['Price'].astype(float) > 0, 'Paid', 'Free')
    # Type encoding
    types = preprocessing.LabelEncoder()
    df_train['Type_LE'] = types.fit_transform(df_train['Type'])
    df_train['Last Updated'].replace('Everyone 10+', np.nan, inplace=True)
    df_train = df_train[pd.notnull(df_train['Last Updated'])]

    df_train['Last Updated'] = df_train['Last Updated'].apply(
        lambda x: time.mktime(datetime.datetime.strptime(x, '%B %d, %Y').timetuple()))

    regex = [r',']
    for j in regex:
        df_train['Size'] = df_train['Size'].astype(
            str).apply(lambda x: re.sub(j, '', x))

    # Convert kbytes to Mbytes
    k_indices = df_train['Size'].loc[df_train['Size'].str.contains(
        'k')].index.tolist()
    converter = pd.DataFrame(df_train.loc[k_indices, 'Size'].apply(lambda x: x.strip(
        'k')).astype(float).apply(lambda x: x / 1024).apply(lambda x: round(x, 3)).astype(str))
    df_train.loc[k_indices, 'Size'] = converter

    # Size cleaning
    df_train['Size'] = df_train['Size'].apply(lambda x: x.strip('M'))
    df_train[df_train['Size'] == 'Varies with device'] = 0
    df_train['Size'] = df_train['Size'].astype(float)

    regex = [r'[-+|/:/;(_)@\[\]#�,>]', r'\s+', r'[A-Za-z]+']
    for j in regex:
        df_train['Minimum Version'] = df_train['Minimum Version'].astype(
            str).apply(lambda x: re.sub(j, '0', x))

    df_train['Minimum Version'] = df_train['Minimum Version'].astype(str).apply(
        lambda x: x.replace('.', ',', 1).replace('.', '').replace(',', '.', 1)[:3]).astype(float)
    df_train['Minimum Version'] = df_train['Minimum Version'].fillna(
        df_train['Minimum Version'].median())
    final_dataset = df_train[df_train['Type'] != 0]
    final_dataset.to_csv('dataset/preprocessed.csv')

    df_train['Price'] = df_train['Price'].astype(float)
    df_train['Rating'] = df_train['Rating'].astype(float)
    df_train['Reviews'] = df_train['Reviews'].astype(int)
    df_train['Last Updated'] = df_train['Last Updated'].astype(float)

    install = preprocessing.LabelEncoder()
    df_train['Installs'] = df_train['Installs'].astype(int)
    df_train['Installs_LE'] = install.fit_transform(df_train['Installs'])

    joblib.dump(types, 'temp/types_label_encoder.joblib')
    joblib.dump(install, 'temp/install_label_encoder.joblib')
    joblib.dump(category, 'temp/category_label_encoder.joblib')
    joblib.dump(content, 'temp/content_label_encoder.joblib')

    return df_train
