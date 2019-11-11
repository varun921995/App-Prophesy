from flask import Blueprint
from flask import Flask, render_template
import pandas as pd
import json
import csv
import pandas as pd
import re
import numpy as np

developer = Blueprint('developer', __name__)

@developer.route("/developerPage")
def main():
    return render_template('developer.html')


@developer.route("/scatterPlot")
def scatterPlot():
    return render_template('scatterplot.html')


@developer.route("/testApi")
def testApi():
    return "list of applications"


@developer.route('/getData', methods=['GET'])
def get_data():
    csvFile = "dataset/Google-Playstore-32K.csv"
    data = {}
    with open(csvFile) as csvF:
        csvReader = csv.DictReader(csvF)
        idx=0
        for rows in csvReader:
           data[idx] = rows
           idx=idx+1
    data = json.dumps(data)
    return (data)

@developer.route('/getDataForScatter', methods=['GET'])
def getDataForScatter():
    csvFile = "dataset/Google-Playstore-32K.csv"
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
        responseDf = df.loc[df['Category'] == "FOOD_AND_DRINK"]
        res['data'] = df.to_json(orient='records')
        res['categories'] =  np.array(categories).tolist()
        res['test'] = {"cate"  : 1}
    return res