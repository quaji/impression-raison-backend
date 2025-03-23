from flask import *
from flask_cors import *
from project.BlueprintManager import BlueprintManager

class App:
    __app :Flask

    def __init__(self, debugMode):
        print("app instance generate.")
        # flaskのメインフレーム起動
        self.__app = Flask(__name__)
        CORS(self.__app,origins=["https://https://lemon-water-022469c10.6.azurestaticapps.net/"])
        self.__app.debug = debugMode
        self.__app.secret_key = 'url1bba'
        self.__app.config.update(
            SESSION_COOKIE_SECURE=False,  # HTTPSでのみCookieを送信
            SESSION_COOKIE_HTTPONLY=True, # JavaScriptからのアクセスを防止
            SESSION_COOKIE_SAMESITE='Lax' # サイト間リクエスト対策
        )

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