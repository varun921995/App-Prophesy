from flask import Blueprint
from flask import Flask, render_template,request
import pandas as pd
import json
import csv
import re
import numpy as np
from flask import jsonify
from collections import OrderedDict
from models.textMining import *

developer = Blueprint('developer', __name__)

@developer.route("/developerPage")
def main():
    return render_template('developer.html')


@developer.route("/scatterPlot")
def scatterPlot():
    return render_template('scatterplot.html')

@developer.route("/correlation")
def correlation():
    return render_template('correlation.html')




@developer.route("/testApi")
def testApi():
    return "list of applications"

@developer.route("/wordCloud")
def wordCloud():
    return render_template('/wordCloud.html')

@developer.route('/getData', methods=['GET'])
def get_data():
    csvFile = "dataset/Google-Playstore-32K.csv"
    data = []
    fieldnames = ("App Name","Category","Rating","Reviews",	"Installs",	"Size",	"Price"	,"Content Rating","Last Updated"	
    ,"Minimum Version","Latest Version")
    with open(csvFile) as csvF:
        csvReader = csv.DictReader(csvF, fieldnames)
        for rows in csvReader:
            entry = OrderedDict()
            for field in fieldnames:
                entry[field] = rows[field]
            data.append(entry)
    data = json.dumps(data)
    return (data)

@developer.route('/getDataForScatter', methods=['GET'])
def getDataForScatter():
    csvFile = "dataset/preprocessed.csv"
    data = {}
    response = []
    res = dict()
    with open(csvFile) as csvF:
        csvReader = csv.DictReader(csvF)
        df = pd.read_csv(csvFile, delimiter=',')
        idx=0
        regex = [r'GAME_[A-Za-z]+.*']
        for j in regex:
            df['Category'] = df['Category'].astype(str).apply(lambda x : re.sub(j, 'GAME', x))
        categories = df['Category'].unique()
        res['data'] = df.to_json(orient='records')
        res['categories'] =  np.array(categories).tolist()
    return res

    
@developer.route("/word-installation-data/<id>")
def callTextMining(id):
    # textMining()
    with open('dataset/dataWithMeaningfulWords.json') as json_file:
        data = json.load(json_file) 
        return data[id]

@developer.route("/getCorrelation")
def getCorrelationMatrix():
    res = dict()
    csvFile = "dataset/preprocessed.csv"
    with open(csvFile) as csvF:
        csvReader = csv.DictReader(csvF)
        df = pd.read_csv(csvFile, delimiter=',', index_col=0)
        # df.drop(['Unnamed: 0'])
        correlationMatrix = getCorrelation(df)
        columnsList = df.columns
        res['columns'] = list(columnsList)
        res['correlation_matrix'] = correlationMatrix
        return jsonify(res)
    
       
def getCorrelation(df):
    corrDf = df.corr()
    df1 = corrDf.stack().reset_index()
    df1.insert(0, 'Value1', pd.factorize(df1['level_0'])[0])
    df1.insert(2, 'Value2', pd.factorize(df1['level_1'])[0])
    df1.drop(['level_0', 'level_1'], axis=1, inplace=True)
    df1  = df1.round(2)
    correlationMatrix = df1.values.tolist()
    return correlationMatrix
