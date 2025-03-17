from flask import *
from project.user_auth.Members import Members
from flask_cors import *
class App:
    __app :Flask

    def __init__(self, debugMode):
        print("app instance generate.")
        self.__app = Flask(__name__)
        CORS(self.__app,origins=["https://your-frontend-app.azurewebsites.net"])
        self.__app.debug = debugMode

    def run(self):
        print("run method in app instance start")
        self.__app.run()