from flask import Blueprint
from flask import Flask, render_template
import pandas as pd
import json
import csv
developer = Blueprint('developer', __name__)

@developer.route("/developerPage")
def main():
    return render_template('developer.html')

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