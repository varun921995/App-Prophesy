from flask import Blueprint
from flask import Flask, render_template

home = Blueprint('home', __name__)

@home.route("/index")
def homepage():
    return render_template('homepage.html')