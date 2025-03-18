from flask import *
from flask_cors import *
from project.BlueprintManager import BlueprintManager

class App:
    __app :Flask

    def __init__(self, debugMode):
        print("app instance generate.")
        # flaskのメインフレーム起動
        self.__app = Flask(__name__)
        CORS(self.__app,origins=["https://your-frontend-app.azurewebsites.net"])
        self.__app.debug = debugMode
        # blueprintManager の設定
        self.blueprintManager = BlueprintManager()
        self.blueprints = self.blueprintManager.get_blueprints()
    
    def __register_blueprints(self):
        for key in self.blueprints:
            self.__app.register_blueprint(self.blueprints[key])
    
    

    def run(self):
        print("run method in app instance start")
        self.__register_blueprints()
        self.__app.run(host="0.0.0.0",port=8000)