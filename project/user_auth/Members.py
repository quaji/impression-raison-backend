from flask import *
from flask_cors import *
import pyodbc
import smtplib
from email.mime.text import MIMEText
import secrets
import os

class Members:
    def __init__(self):
        self.__blueprint = Blueprint('sign', __name__, url_prefix='/sign')
        self.__setDBStatus()
        self.__sign()

    def get_blueprint(self):
        return self.__blueprint

    def __setDBStatus(self):
        SERVER = os.getenv('db_server')
        DATABASE = os.getenv('db_name_members')
        USERNAME = 'Quaji'
        PASSWORD = os.getenv('member_pass')
        connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server={SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.conn.cursor()

    def __send_check_mail(self, to_email :str):
        randnum = secrets.randbelow(9000) + 1000
        session['tempCode'] = randnum
        from_email = os.getenv('AUTO_MAIL')

        print("make code")
        
        body =f"""
        impression-raison にメールアドレスでサインアップしている方にこのメールは自動送信されています。

        以下の4桁の一時コードをサインイン画面の一番上の入力欄に入力してください。また、不正メールにご注意ください。

        一時コード:{randnum}

        ページをリロードした場合、一時コードが再設定およびメールが再送されます。
        """
        print("make body")

        message = MIMEText(body)
        message['Subject'] = 'impression-raison 登録確認メールの送信'
        message['From'] = from_email
        message['To'] = to_email
        password = os.getenv('PASSWORD_AUTO_MAIL')
        print("make mail")
        

        server = smtplib.SMTP('smtp.gmail.com',587)
        print("make code")

        server.starttls()
        print("make code")
        server.login(from_email,password)
        print("make code")
        server.send_message(message)
        print("make code")
        server.quit()
        print("make code")
        session.modified = True




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

                print(f'catch request data')

                SQLquery = """
                    SELECT *
                    FROM Members
                    WHERE email=?
                """

                self.cursor.execute(SQLquery, (email,))
                existingData = self.cursor.fetchone()

                print(f'done sql query')


                if existingData is None:
                    print(f'data not existing')
                    session["email"] = email
                    session.modified = True
                    self.__send_check_mail(email)
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signup'}),200
                else:
                    print(f'data existing: {existingData}')
                    session["email"] = existingData.email
                    session.modified = True
                    return jsonify({'link':'https://lemon-water-022469c10.6.azurestaticapps.net/signin'}),200
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
                    return jsonify({"message": "Password doesn't match"}), 201
            except Exception as e:
                return jsonify({"message": f"Error occurred: {str(e)}"}), 500
        


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
                    return jsonify({"message": "Password doesn't register"}), 201
            except Exception as e:
                return jsonify({"message": f"Error occurred: {str(e)}"}), 500
