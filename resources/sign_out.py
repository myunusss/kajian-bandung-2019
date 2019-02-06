from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
import hashlib

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
sessionToken="session_token"
detail="detail"

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
        
        try:
            conn, cur = ConnectDB()

            cur.execute("select therapist_id from therapist where login_id = %s", [username])
            data = cur.fetchone()

            if (data != None):
                therapist_id = data[0]

                # print("THERAPIST ID ", therapist_id)
                result = []

                if (therapist_id == 0):
                    result = jsonify(response_code="401", response_text="User not found")

                else:
                    cur.execute("select user_token from ther_session where therapist_id = %s and device_id = %s and logout_time is null limit 1", [therapist_id, device_id])
                    dataSession = cur.fetchone()

                    if (dataSession != None):
                        user_token = dataSession[0]
                        valid_token = hashlib.md5(user_token+device_id.encode())

                        if (session_token == valid_token.hexdigest()):
                            cur.execute("update ther_session set logout_time = current_timestamp where therapist_id = %s and device_id = %s and user_token = %s and logout_time is null", [therapist_id, device_id, user_token])
                            conn.commit()

                            result = {responseCode:"200", responseText:"Success"}
                        else:
                            result = {responseCode:"401", responseText:"Not valid token"}
                    else:
                        result = {responseCode:"401", responseText:"Not found"}
            else:
                result = {responseCode:"401", responseText:"Sign out failed"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)
        
        return result