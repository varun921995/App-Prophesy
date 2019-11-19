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
from models.preprocessing import preProcessData 
import random
import xgboost as xgb


def trainModelRating(df_train):
    
    # Split data into training and testing sets
    features = [ 'Size', 'Type_LE', 'ContentRating_LE','Price','Category_LE']
    # features.extend(category_list)
    X = df_train[features]
    y = df_train['Rating']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 10)

    xgbModel = xgb.XGBRegressor()
    xgbModel.fit(X_train, y_train)
    accuracy = xgbModel.score(X_test,y_test)
    print('Accuracy: ' + str(np.round(accuracy*100, 2)) + '%')
    return xgbModel

def trainModelInstallation(df_train):
    df_train = preProcessData()
    # Split data into training and testing sets
    features = [ 'Size', 'Type_LE', 'ContentRating_LE','Price','Category_LE']
    # features.extend(category_list)
    X = df_train[features]
    y = df_train['Installs_LE']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 10)


    xgbModel = xgb.XGBRegressor()
    xgbModel.fit(X_train, y_train)
    accuracy = xgbModel.score(X_test,y_test)
    print('Accuracy: ' + str(np.round(accuracy*100, 2)) + '%')
    return xgbModel
