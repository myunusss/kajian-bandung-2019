from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
import hashlib
from common.app_setting import responseCode, responseText, detail

app = Flask(__name__)

class SignOut(Resource):
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
        
        conn, cur = ConnectDB()
        try:
            cur.execute("select therapist_id from ther_session where logout_time is null and user_token = %s", [session_token])
            data = cur.fetchone()

            if (data != None):
                therapist_id = data[0]

                result = []

                cur.execute("select user_token from ther_session where therapist_id = %s and device_id = %s and logout_time is null limit 1", [therapist_id, device_id])
                dataSession = cur.fetchone()

                if (dataSession != None):
                    user_token = dataSession[0]

                    if (session_token == user_token):
                        cur.execute("update ther_session set logout_time = current_timestamp where therapist_id = %s and device_id = %s and user_token = %s and logout_time is null", [therapist_id, device_id, user_token])
                        conn.commit()

                        result = {responseCode:"200", responseText:"Success"}
                    else:
                        result = {responseCode:"401", responseText:"Not valid token"}
                else:
                    result = {responseCode:"401", responseText:"Not found"}
            else:
                # Jika session di database sudah tidak ada recordnya, maka diloloskan saja, langsung masuk ke login
                result = {responseCode:"200", responseText:"Success with exception"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)
        
        return result