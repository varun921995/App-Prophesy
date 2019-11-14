from flask import Blueprint
from flask import Flask, render_template
import pandas as pd
import json
import csv
from collections import OrderedDict
from models.textMining import *
from flask import Flask, request

developer = Blueprint('developer', __name__)

@developer.route("/developerPage")
def main():
    return render_template('developer.html')

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

@developer.route("/word-installation-data/<id>")
def callTextMining(id):
    # textMining()
    with open('dataset/dataWithMeaningfulWordsNorm2.json') as json_file:
        data = json.load(json_file) 
        return data[id]

