from flask import *
from flask_cors import *
import pyodbc
class Members:
    def __init__(self):
        self.__blueprint = Blueprint('sign',__name__,url_prefix='/sign')
        CORS(self.__blueprint)
        self.__setDBStatus()
        self.__sign()

    def __setDBStatus(self):
        SERVER = 'tcp:impression-raison-backend.database.windows.net'
        DATABASE = 'Members'
        USERNAME = 'Quaji'
        PASSWORD = 'H!E!RBV8yGWN:Wc'
        connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        conn = pyodbc.connect(connectionString)
        self.cursor = conn.cursor()

    def __sign(self):
        @self.__blueprint.route('/auth',method=['GET'])
        def authentication():
            try:
                usr :dict = json.loads(request.data.decode('utf-8'))
                email :str = usr["email"]
                password :str = usr["password"]

                SQLquery = """

"""
                if True:
                    return jsonify({'message':'YOU ARE MEMBER'}),100
                else:
                    return jsonify({'message':'AGREE REGI'}),101
            except:
                return jsonify({'message': 'HAPPEN ERROR'}),38808