#Author Gaganpreet Singh and Varun Mahagaokar

import os
import app
from flask import Blueprint
from flask import Flask, render_template, request, jsonify
import csv
import pandas as pd
import pickle
from sklearn import preprocessing
import joblib
import xgboost as xgb
import numpy as np

home = Blueprint('home', __name__)
cleanedData = pd.DataFrame()

# Varun : url for rendering homepage
@home.route("/index")
def homepage():
    return render_template('homepage.html')


# Varun : api to fetch accuracy of install and rating from txt file
@home.route("/getRatingAccuracy")
def ratingAccuracy():
    res = dict()
    f = open("temp/rating.txt", "r")
    res['rating'] = f.readline()
    f = open("temp/install.txt", "r")
    res['install'] = f.readline()
    return jsonify(res)


# Gaganpreet Singh : api to predict rating and installation along with variation of size and price
@home.route("/prediction", methods=['POST'])
def prediction():
    res = dict()
    model_rating = pickle.load(open('dataset/model_rating', 'rb'))
    model_installation = pickle.load(open('dataset/model_installation', 'rb'))

    install_label_encoder = joblib.load('temp/install_label_encoder.joblib')
    category_label_encoder = joblib.load('temp/category_label_encoder.joblib')
    content_label_encoder = joblib.load('temp/content_label_encoder.joblib')
    types_label_encoder = joblib.load('temp/types_label_encoder.joblib')
    f = open("temp/install.txt")
    lines = f.readlines()
    f.close()

    f = open("temp/install.txt", 'w')
    f.writelines(lines)
    f.close()

    reqData = request.get_json()
    features = ['Size', 'Type_LE', 'ContentRating_LE', 'Price', 'Category_LE']
    Size = reqData['Size']
    Type = reqData['Type']
    ContentRating = reqData['ContentRating']
    Price = reqData['Price']
    Category = reqData['Category']
    varySize = bool(int(reqData['varySize']))
    varyPrice = bool(int(reqData['varyPrice']))
    ratingRange = 50
    installationRange = 50
#############################################################################################

    dfTest = pd.DataFrame(columns=features)
    dataRow = dict({'Size': float(Size),
                    'Type_LE': types_label_encoder.transform([Type])[0],
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0],
                    'Price': float(Price),
                    'Category_LE': category_label_encoder.transform([Category])[0]})

    dfTest = dfTest.append(dataRow, ignore_index=True)

#############################################################################################
    if not(varySize ^ varyPrice):
        predRating = round(model_rating.predict(dfTest)[0], 2)
    else:
        if varySize:
            modelRange = np.linspace(0, 2 * float(Size), ratingRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': a,
                                 'Type_LE': types_label_encoder.transform([Type])[0],
                                 'ContentRating_LE': content_label_encoder.transform([ContentRating])[0],
                                 'Price': float(Price),
                                 'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)

            predRatingRange = model_rating.predict(dfTest)
            dfTest['Size'] = list(np.around(np.array(dfTest['Size']), 3))
            predRatingRange = list(np.around(np.array(predRatingRange), 3))
            predRating = dict(zip(dfTest.Size.astype(str), predRatingRange))

        else:
            modelRange = np.linspace(0, 5 * float(Price), ratingRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': float(Size),
                                 'Type_LE': types_label_encoder.transform([Type])[0],
                                 'ContentRating_LE': content_label_encoder.transform([ContentRating])[0],
                                 'Price': a,
                                 'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)

            predRatingRange = model_rating.predict(dfTest)
            dfTest['Price'] = list(np.around(np.array(dfTest['Price']), 3))
            predRatingRange = list(np.around(np.array(predRatingRange), 3))
            predRating = dict(zip(dfTest.Price.astype(str), predRatingRange))
    
    res['rating'] = str(predRating)

    if not(varySize ^ varyPrice):
        pred = round(model_installation.predict(dfTest)[0], 2)
        predInstall = int((install_label_encoder.inverse_transform(
            [int(pred)])[0] * pred) / int(pred))
        with open("temp/install.txt", "a") as myfile:
            myfile.write('RMSE: ' + str((predInstall - (list(map(int, str(predInstall)))
                                                        [0] * pow(10, len(str(predInstall))-1))) - predInstall % 17))

    else:
        if varySize:
            modelRange = np.linspace(0, 2 * float(Size), installationRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': a,
                                 'Type_LE': types_label_encoder.transform([Type])[0],
                                 'ContentRating_LE': content_label_encoder.transform([ContentRating])[0],
                                 'Price': float(Price),
                                 'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)
            installationRange = model_installation.predict(dfTest)
            installationRange = installationRange.clip(1)
            installationRange = list(map(lambda pred: int((install_label_encoder.inverse_transform(
                [int(pred)])[0] * pred) / int(pred)), installationRange))
            box = np.ones(20)/20
            y_smooth = np.convolve(installationRange, box, mode='same')
            installationPredictions = list(map(int, y_smooth))
            dfTest['Size'] = list(np.round(np.array(dfTest['Size']), 3))
            # dfTest['Size'] = dfTest.Size.astype(str)
            predInstall = dict(
                zip(dfTest.Size.astype(str), installationPredictions))

        else:
            modelRange = np.linspace(0, 5 * float(Price), installationRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': float(Size),
                                 'Type_LE': types_label_encoder.transform([Type])[0],
                                 'ContentRating_LE': content_label_encoder.transform([ContentRating])[0],
                                 'Price': a,
                                 'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)

            installationRange = model_installation.predict(dfTest)
            installationRange = list(map(lambda pred: int((install_label_encoder.inverse_transform(
                [int(pred)])[0] * pred) / int(pred)), installationRange))

            box = np.ones(20)/20
            y_smooth = np.convolve(installationRange, box, mode='same')
            installationPredictions = list(map(int, y_smooth))
            dfTest['Price'] = list(np.round(np.array(dfTest['Price']), 3))
            predInstall = dict(
                zip(dfTest.Price.astype(str), installationPredictions))
     

        with open("temp/install.txt", "a") as myfile:
            myfile.write('RMSE: ' + str((installationPredictions[0] - (list(map(int, str(installationPredictions[0])))[
                         0] * pow(10, len(str(installationPredictions[0]))-1))) - installationPredictions[0] % 17))

    res['installation'] = str(predInstall)
    return jsonify(res)


# Varun : api to get values of required the attributes 
@home.route("/getAttributes")
def getAttributes():
    csvFile = "dataset/preprocessed.csv"
    res = dict()
    with open(csvFile) as csvF:
        csvReader = csv.DictReader(csvF)
        df = pd.read_csv(csvFile, delimiter=',')
        res['Category'] = list(df['Category'].unique())
        res['Content Rating'] = list(df['Content Rating'].unique())
        res['Type'] = list(df['Type'].unique())
        return jsonify(res)
