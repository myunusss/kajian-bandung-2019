from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB

todos = {}

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

class ListTherapistStatus(Resource):
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
            data = [
                {str("id"):str("0"), str("label"):str("Off/Rest")},
                {str("id"):str("1"), str("label"):str("Available")},
                {str("id"):str("2"), str("label"):str("Prepare")}
            ]

            result = {
                responseCode:"200", responseText:"Success", responseList:data
            }

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}

        return result

class UpdateTherapistStatus(Resource):
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

        if (request.form.get("status_id") != None):
            status_id = request.form.get("status_id")
        else:
            status_id = ""

        try:
            conn, cur = ConnectDB()
            cur.execute("select therapist_id, therapist_status from therapist where login_id = %s", [username])
            
            data = cur.fetchone()
            therapist_id = data[0]
            db_status_id = data[1]

            if (db_status_id != 3):
                cur.execute("update therapist set therapist_status = %s where " +
                "therapist_id in (select therapist_id from therapist where login_id = %s) ", [status_id, username])
                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else :
                result = {responseCode:"404", responseText:"Maaf anda sedang berada pada status working"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result