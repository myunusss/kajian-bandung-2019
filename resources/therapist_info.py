from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail, URL_IMAGE, URL_REPORTS
from datetime import datetime, timedelta, time

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
            cur.execute("select therapist_id, therapist_status, therapist_no, coalesce(alias_name,'-'), thumbnail_image " +
                "from ther_session " +
                "inner join therapist using(therapist_id) " +
                "where logout_time is null and user_token = %s ", [session_token])
            
            data = cur.fetchone()
            # print('data', data)
            if (data != None):
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

                cur.execute("select to_char(clock_in, 'YYYY-MM-DD HH24:MI:SS'::text) from attendance where therapist_id = %s order by clock_in desc limit 1", [therapist_id])
                dataAttend = cur.fetchone()[0]

                # print('data attend', dataAttend)

                if dataAttend != None :
                    FMT = '%Y-%m-%d %H:%M:%S'
                    now = str(datetime.now().strftime(FMT))
                    # now_str = '2019-06-27 06:00:00' // buat test, atur jam nya
                    # now_obj = datetime.strptime(now_str, FMT)
                    date_time_obj = datetime.strptime(dataAttend, FMT)
                    date2 = datetime.combine(date_time_obj.date(), time(23, 59, 59))
                    # intervalTime = datetime.strptime(now, FMT) - datetime.strptime(dataAttend, FMT)
                    newInterval = datetime.strptime(now, FMT) - date2
                    total_sec = newInterval.total_seconds()
                    # print('sec', total_sec)
                    h = total_sec//3600
                    # m = (total_sec%3600) // 60
                    # print('attend', dataAttend)
                    # print('now', now)
                    # print('end time', date2)
                    # print "%d:%d" %(h,m)
                    # print('h', h)
                    if h > 5:
                        isAttend = False
                    else:
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
            else :
                result = {responseCode:"404", responseText:"Failed", detail:"Not found"}

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)
        # print(result)
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

                url_report = URL_REPORTS + str(therapist_id)

                result = {responseCode:"200", responseText:"Success", detail:str(url_report)}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}
        
        finally:
            CloseDB(conn, cur)

        return result