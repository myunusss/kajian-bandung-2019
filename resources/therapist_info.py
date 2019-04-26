from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail, URL_IMAGE

app = Flask(__name__)

class TherapistInfo(Resource):
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
            cur.execute("select therapist_id, therapist_status, therapist_no, therapist_name, thumbnail_image " +
                "from ther_session " +
                "inner join therapist using(therapist_id) " +
                "where logout_time is null and user_token = %s ", [session_token])
            
            data = cur.fetchone()
            therapist_id = data[0]
            status_id = data[1]
            therapist_no = data[2]
            therapist_name = data[3]
            image = data[4]

            if (status_id == 0):
                therapist_status = "Off/Rest"
                therapist_status_color = "#f22c21" #red
            elif (status_id == 1):
                therapist_status = "Available"
                therapist_status_color = "#2cff00" #green
            elif (status_id == 2):
                therapist_status = "Prepare"
                therapist_status_color = "#ff8500" #orange
            elif (status_id == 3):
                therapist_status = "Working"
                therapist_status_color = "#008aff" #blue
            elif (status_id == 4):
                therapist_status = "Booked"
                therapist_status_color = "#8558e3" #ungu muda
            else :
                therapist_status = "Unknown"
                therapist_status_color = "#000" #hitam

            cur.execute("select clock_in from attendance where therapist_id = %s and clock_in::date = current_date", [therapist_id])
            data = cur.fetchone()
            if data != None :
                isAttend = True
            else :
                isAttend = False

            result = {
                responseCode:"200", responseText:"Success",
                "ther_id":str(therapist_id), "ther_status":str(therapist_status),
                "ther_color":str(therapist_status_color), "ther_status_id":str(status_id),
                "ther_no":str(therapist_no), "ther_name":str(therapist_name),
                "image":str(URL_IMAGE+image), "isAttend":isAttend
            }

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)
        
        return result


class TherapistReport(Resource):
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
            if (username != "" and session_token != "" and device_id != ""):

                cur.execute("select therapist_id, therapist_no, therapist_name " +
                "from ther_session " +
                "inner join therapist using(therapist_id) " +
                "where logout_time is null and user_token = %s ", [session_token])
            
                data = cur.fetchone()
                therapist_id = data[0]
                therapist_no = data[1]
                therapist_name = data[2]

                url_report = "http://192.168.1.221:8000/therapist/report?ther_id=" + str(therapist_id)

                result = {responseCode:"200", responseText:"Success", detail:str(url_report)}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}
        
        finally:
            CloseDB(conn, cur)

        return result