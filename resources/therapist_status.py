from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail, responseList

todos = {}

app = Flask(__name__)

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
                {str("id"):str("1"), str("label"):str("Available")}
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

        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = 0

        conn, cur = ConnectDB()
        try:
            # cur.execute("select therapist_id, therapist_status from therapist where login_id = %s", [username])
            
            # data = cur.fetchone()
            # therapist_id = data[0]
            # db_status_id = data[1]

            cur.execute("update therapist set therapist_status = %s where " +
            "therapist_id = %s", [status_id, ther_id])

            count = cur.rowcount
            
            if (count != 0):
                conn.commit()
                result = {responseCode:"200", responseText:"Success"}
            else :
                conn.rollback()
                result = {responseCode:"401", responseText:"Failed update / insert data"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result