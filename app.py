from flask import Flask, render_template, request
from flask_cors import CORS
from routes.Developer import developer
from routes.Homepage import *

from models.preprocessing import *
from models.model import *
import pickle

from routes.sburst import sunburst
def create_app():
    app = Flask(__name__)
    app.register_blueprint(developer)
    app.register_blueprint(sunburst)
    app.register_blueprint(home)
    # global cleanedData
    cleanedData = preProcessData()
    print("Completed: Data Cleaning")
    model_rating = trainModelRating(cleanedData)
    pickle.dump(model_rating, open('dataset/model_rating', 'wb'))
    print("Completed: Model Training for Rating")

    model_installation = trainModelInstallation(cleanedData)
    pickle.dump(model_installation, open('dataset/model_installation', 'wb'))
    print("Completed: Model Training for installation")

    CORS(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug= True, host='0.0.0.0')
    return app


if __name__ == "__main__":
    create_app()
    