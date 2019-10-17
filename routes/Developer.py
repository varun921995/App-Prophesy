from flask import Blueprint
from flask import Flask, render_template

developer = Blueprint('developer', __name__)

@developer.route("/developerPage")
def main():
    return render_template('developer.html')

@developer.route("/testApi")
def testApi():
    return "list of applications"