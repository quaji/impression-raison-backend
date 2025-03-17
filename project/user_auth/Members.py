from flask import *
from flask_cors import *
import pyodbc

class Members:
    def __init__(self):
        self.__blueprint = Blueprint('sign', __name__, url_prefix='/sign')
        CORS(self.__blueprint)
        self.__setDBStatus()
        self.__sign()

    def __setDBStatus(self):
        SERVER = 'tcp:impression-raison-backend.database.windows.net'
        DATABASE = 'Members'
        USERNAME = 'Quaji'
        PASSWORD = 'H!E!RBV8yGWN:Wc'
        connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.conn.cursor()

    def __sign(self):
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
                    session["email"] = existingData.email
                    return redirect("https://passwordを認証するページ")
                else:
                    return redirect("https://passwordを設定するページ")
            except Exception as e:
                return jsonify({'message': f'Error occurred: {str(e)}'}), 1001

        @self.__blueprint.route('/in', methods=['POST'])
        def signin():
            try:
                if "email" not in session:
                    return redirect("https://emailを入力するページ")

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
                    return redirect("https://example.com/mainpage")
                else:
                    return jsonify({"message": "Password doesn't match"}), 1002
            except Exception as e:
                return jsonify({"message": f"Error occurred: {str(e)}"}), 1003