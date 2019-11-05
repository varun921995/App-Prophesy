from flask import Flask, render_template, request
from flask_cors import CORS
from routes.Developer import developer
from routes.Homepage import home
from models.test import *
def create_app():
    app = Flask(__name__)
    app.register_blueprint(developer)
    app.register_blueprint(home)
    CORS(app)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug= True, host='0.0.0.0')
    return app

# app = Flask(__name__)



# @app.route("/sunburst")
# def sunburstGraph():
#     return render_template('sunburst.html')

# @app.route("/radialGraph")
# def radialGraph():
#     return render_template('radialGraph.html')

# @app.route('/getfile', methods=['GET','POST'])
# def getfile():
#         with open("templates/winequality-red.csv") as f:
#             file_content = f.read()
#         return file_content 

if __name__ == "__main__":
    main()
    create_app()