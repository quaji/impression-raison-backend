from flask import *
from user_auth.Members import Members
from flask_cors import *
class App:
    __app :Flask

    def __init__(self, debugMode):
        print("app instance generate.")
        self.__app = Flask(__name__)
        CORS(self.__app)
        self.__app.debug = debugMode

    def run(self):
        print("run method in app instance start")
        self.__app.run()