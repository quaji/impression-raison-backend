from flask import *
from flask_cors import *
from flask_session import *
from project.BlueprintManager import BlueprintManager
from datetime import timedelta

class App:
    __app :Flask

    def __init__(self, debugMode):
        print("app instance generate.")
        # flaskのメインフレーム起動
        self.__app = Flask(__name__)
        CORS(self.__app,origins=["https://lemon-water-022469c10.6.azurestaticapps.net/"],supports_credentials=True)
        self.__app.debug = debugMode
        self.__app.secret_key = 'url1bba'
        self.__app.config.update(
            SESSION_TYPE="filesystem",
            SESSIOM_FILE_DIR="/project/flask_session",
            SESSION_PERMANENT = True,
            SESSION_COOKIE_SECURE=True,  # HTTPSでのみCookieを送信
            SESSION_COOKIE_HTTPONLY=True, # JavaScriptからのアクセスを防止
            SESSION_COOKIE_SAMESITE='Lax', # サイト間リクエスト対策
            PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
        )
        Session(self.__app)

        # blueprintManager の設定
        self.blueprintManager = BlueprintManager()
        self.blueprints = self.blueprintManager.get_blueprints()
        self.__register_blueprints()
    
    def __register_blueprints(self):
        for key in self.blueprints:
            self.__app.register_blueprint(self.blueprints[key])
    
    def get_app(self):
        return self.__app


    def run(self):
        self.__app.run()