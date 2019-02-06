from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from flask_bcrypt import Bcrypt
import hashlib

todos = {}

app = Flask(__name__)
bcrypt = Bcrypt(app)

responseCode="response_code"
responseText="response_text"
sessionToken="session_token"
detail="detail"

class ChangePassword(Resource):
    def post(self):

        if (request.form.get("uname") != None):
            username = request.form.get("uname")
        else:
            username = ""

        if (request.form.get("stkn") != None):
            session_token = request.form.get("stkn")
        else:
            session_token = ""
        
        if (request.form.get("di") != None):
            device_id = request.form.get("di")
        else:
            device_id = ""
        
        if (request.form.get("password") != None):
            password = request.form.get("password")
        else:
            password = ""

        if (request.form.get("new_password") != None):
            new_password = request.form.get("new_password")
        else:
            new_password = ""

        try:
            conn, cur = ConnectDB()
            cur.execute("select therapist_id, login_password from therapist where login_id = %s", [username])
            data = cur.fetchone()

            print("DATA", data)
            if (data != None):
                therapist_id = data[0]
                therapist_pass = data[1]

                if (bcrypt.check_password_hash(therapist_pass, password)):
                    pw_hash = bcrypt.generate_password_hash(new_password)

                    cur.execute("update therapist set login_password = %s where therapist_id = %s", [pw_hash, therapist_id])

                    conn.commit()
                    result = {responseCode:"200", responseText:"Success"}
                else:
                    result = {responseCode:"401", responseText:"Wrong Password"}
            else:
                result = {responseCode:"401", responseText:"Username undefined"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result