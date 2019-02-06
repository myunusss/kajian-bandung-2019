from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

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

        try:
            conn, cur = ConnectDB()
            cur.execute("select therapist_id, therapist_status, therapist_no, therapist_name, thumbnail_image from therapist where login_id = %s", [username])
            
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

            result = {
                responseCode:"200", responseText:"Success",
                "ther_id":str(therapist_id), "ther_status":str(therapist_status),
                "ther_color":str(therapist_status_color), "ther_status_id":str(status_id),
                "ther_no":str(therapist_no), "ther_name":str(therapist_name),
                "image":str("http://192.168.1.221:8000"+image)
            }

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result