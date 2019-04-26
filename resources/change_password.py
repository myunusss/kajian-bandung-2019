from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from flask_bcrypt import Bcrypt
import hashlib
from common.app_setting import responseCode, responseText, detail

todos = {}

app = Flask(__name__)
bcrypt = Bcrypt(app)

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

        conn, cur = ConnectDB()
        try:
            cur.execute("select t.therapist_id, t.login_password from therapist t left join ther_session ts on t.therapist_id = ts.therapist_id " +
            "where lower(login_id) = lower(trim(%s)) and coalesce(suspended,0) = 0 " +
            "and ts.user_token = (select user_token from ther_session where user_token = %s and logout_time is null) " +
            "limit 1", [username, session_token])
            data = cur.fetchone()

            if (data != None):
                therapist_id = data[0]
                therapist_pass = data[1]

                if (bcrypt.check_password_hash(therapist_pass, password)):
                    pw_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

                    cur.execute("update therapist set login_password = %s where therapist_id = %s", [pw_hash, therapist_id])

                    result = {responseCode:"200", responseText:"Success"}
                else:
                    result = {responseCode:"401", responseText:"Wrong Password"}
            else:
                result = {responseCode:"401", responseText:"Username undefined"}

            conn.commit()
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result