from flask import *
from flask_cors import *
import pyodbc

class Members:
    def __init__(self):
        self.__blueprint = Blueprint('sign', __name__, url_prefix='/sign')
        self.__setDBStatus()
        self.__sign()

    def get_blueprint(self):
        return self.__blueprint

    def __setDBStatus(self):
        SERVER = 'tcp:impression-raison-backend.database.windows.net'
        DATABASE = 'Members'
        USERNAME = 'Quaji'
        PASSWORD = 'H!E!RBV8yGWN:Wc'
        connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.conn.cursor()

    def __sign(self):
        @self.__blueprint.route('/auth', methods=['GET'])
        def authorization():
            if "uid" in session:
                return jsonify({'uid':session["uid"],'link':"https://lemon-water-022469c10.6.azurestaticapps.net/home"}),200
            else:
                return jsonify({'uid':0,'link':None}),201
        
        @self.__blueprint.route('/auth', methods=['POST'])
        def authentication():
            try:
                usrAddr: dict = request.get_json()
                email: str = usrAddr["email"]

                SQLquery = """
                    SELECT *
                    FROM Members
                    WHERE email=?
                """

                self.cursor.execute(SQLquery, (email,))
                existingData = self.cursor.fetchone()
                if existingData:
                    # session["email"] = existingData.email
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signin'}),200
                else:
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signup'}),200
            except Exception as e:
                return jsonify({'message': f'Error occurred: {str(e)}'}), 500



        @self.__blueprint.route('/in', methods=['POST'])
        def signin():
            try:
                if "email" not in session:
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signin'}),202

                usrPass: dict = request.get_json()
                password: str = usrPass["password"]

                SQLquery = """
                    SELECT *
                    FROM Members
                    WHERE email=? AND password=?
                """

                self.cursor.execute(SQLquery, (session["email"], password,))
                existingData = self.cursor.fetchone()
                if existingData:
                    session["uid"] = existingData.uid
                    session["name"] = existingData.name
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/home'})
                else:
                    return jsonify({"message": "Password doesn't match"}), 1002
            except Exception as e:
                return jsonify({"message": f"Error occurred: {str(e)}"}), 1003
        
        @self.__blueprint.route('/up', methods=['POST'])
        def signup():
            try:
                if "email" not in session:
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signin'}),202

                # username,password登録フェーズ
                usrPass: dict = request.get_json()
                password: str = usrPass["password"]
                username: str = usrPass["username"]

                SQLquery="""
                    データを入力するSQLの記述をする
                """

                self.cursor.execute(SQLquery,(session['email'],password,username,))

                # UIDの取得フェーズ
                SQLquery = """
                    SELECT *
                    FROM Members
                    WHERE email=? AND password=?
                """

                self.cursor.execute(SQLquery, (session["email"], password,))
                existingData = self.cursor.fetchone()

                if existingData:
                    session["email"] = existingData.email
                    session["uid"] = existingData.uid
                    session["name"] = existingData.name
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/home'})
                else:
                    return jsonify({"message": "Password doesn't register"}), 1002
            except Exception as e:
                return jsonify({"message": f"Error occurred: {str(e)}"}), 1004
