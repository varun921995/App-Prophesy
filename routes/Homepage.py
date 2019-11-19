from flask import Blueprint
from flask import Flask, render_template,request,jsonify
import csv
import pandas as pd
import pickle
from sklearn import preprocessing
import joblib
import xgboost as xgb
import numpy as np

home = Blueprint('home', __name__)
cleanedData = pd.DataFrame()

# from app import cleanedData, model_rating, model_installation
import app



@home.route("/index")
def homepage():
    print("Hello")
    return render_template('homepage.html')


@home.route("/prediction", methods=['POST'])
def prediction():
    model_rating = pickle.load(open('dataset/model_rating', 'rb'))
    model_installation = pickle.load(open('dataset/model_installation', 'rb'))
 
    install_label_encoder = joblib.load('temp/install_label_encoder.joblib')
    category_label_encoder = joblib.load('temp/category_label_encoder.joblib')
    content_label_encoder = joblib.load('temp/content_label_encoder.joblib')
    types_label_encoder = joblib.load('temp/types_label_encoder.joblib')


    reqData = request.get_json()
    features = [ 'Size', 'Type_LE', 'ContentRating_LE','Price','Category_LE']
#############################################################################################
    Size = reqData['Size']
    Type = reqData['Type']
    ContentRating = reqData['ContentRating']
    Price = reqData['Price']
    Category = reqData['Category']
    # varySize = bool(int(reqData['varySize']))
    # varyPrice = bool(int(reqData['varyPrice']))
    varyPrice = True
    varySize = False
    ratingRange = 100
    installationRange = 100
#############################################################################################

    dfTest = pd.DataFrame(columns=features)
    dataRow = dict({'Size':float(Size), 
                    'Type_LE':types_label_encoder.transform([Type])[0], 
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0], 
                    'Price': float(Price), 
                    'Category_LE': category_label_encoder.transform([Category])[0]})

    dfTest = dfTest.append(dataRow, ignore_index=True)

#############################################################################################
    if not(varySize^varyPrice):
        predRating = round(model_rating.predict(dfTest)[0],2)
    else:
        if varySize:
            modelRange = np.linspace(0, 2 * int(Size),ratingRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': a, 
                    'Type_LE':types_label_encoder.transform([Type])[0], 
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0], 
                    'Price': float(Price), 
                    'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)
                    
            predRatingRange = model_rating.predict(dfTest)
            predRating = dict(zip(dfTest['Size'], predRatingRange))
            
        else:
            modelRange = np.linspace(0, 5 * float(Price),ratingRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': float(Size), 
                    'Type_LE':types_label_encoder.transform([Type])[0], 
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0], 
                    'Price': a, 
                    'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)
        
            predRatingRange = model_rating.predict(dfTest)
            predRating = dict(zip(dfTest['Price'], predRatingRange))

    print(predRating)
#############################################################################################
    # del(dfTest)
    # dfTest = pd.DataFrame(columns=features)
    # dataRow = dict({'Size':int(Size), 
    #                 'Type':types.transform([Type])[0], 
    #                 'Content Rating': le.transform([ContentRating])[0], 
    #                 'Price': float(Price), 
    #                 'Category': le2.transform([Category])[0]})

    # dfTest = dfTest.append(dataRow, ignore_index=True)

    if not(varySize^varyPrice):
        pred = round(model_installation.predict(dfTest)[0],2)
        predInstall =  int((install_label_encoder.inverse_transform([int(pred)])[0] * pred) / int(pred))
    else:
        if varySize:
            modelRange = np.linspace(0, 2 * int(Size),installationRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': a, 
                    'Type_LE':types_label_encoder.transform([Type])[0], 
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0], 
                    'Price': float(Price), 
                    'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)
            installationRange = model_installation.predict(dfTest)
            installationRange = installationRange.clip(1)
            installationRange = list(map(lambda pred : int((install_label_encoder.inverse_transform([int(pred)])[0] * pred) / int(pred)), installationRange))
            box = np.ones(20)/20
            y_smooth = np.convolve(installationRange, box, mode='same')
            installationPredictions = list(map(int, y_smooth))
            
            predInstall = dict(zip(dfTest['Size'], installationPredictions))

        else:
            modelRange = np.linspace(0, 5 * float(Price),installationRange)
            lst_dict = []
            for a in modelRange:
                lst_dict.append({'Size': float(Size), 
                    'Type_LE':types_label_encoder.transform([Type])[0], 
                    'ContentRating_LE': content_label_encoder.transform([ContentRating])[0], 
                    'Price': a, 
                    'Category_LE': category_label_encoder.transform([Category])[0]})
            dfTest = dfTest.append(lst_dict, ignore_index=True)
            
            installationRange = model_installation.predict(dfTest)
            installationRange = list(map(lambda pred : int((install_label_encoder.inverse_transform([int(pred)])[0] * pred) / int(pred)), installationRange))

            box = np.ones(20)/20
            y_smooth = np.convolve(installationRange, box, mode='same')
            installationPredictions = list(map(int, y_smooth))

            predInstall = dict(zip(dfTest['Price'], installationPredictions))
    print(predInstall)
    return "done"

    
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
        # res['Category'] = df['Category'].unique()
        return jsonify(res)


    
    
    