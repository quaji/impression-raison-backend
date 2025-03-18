from flask import *
from project.user_auth.Members import Members
from flask_cors import *
class App:
    __app :Flask
    __members :Members

    def __init__(self, debugMode):
        print("app instance generate.")
        self.__app = Flask(__name__)
        CORS(self.__app,origins=["https://your-frontend-app.azurewebsites.net"])
        self.__app.debug = debugMode

    def __wake_up(self):
        self.__members = Members()

    def run(self):
        self.__wake_up()
        print("run method in app instance start")
        self.__app.run(host="0.0.0.0",port=8000)