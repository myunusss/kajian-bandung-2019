from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail, responseList

app = Flask(__name__)

class BookingList(Resource):
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
                # FROM SP
                cur.execute("select * from ther_get_booking_list(%s)", [session_token])

                rows = []
                data = []

                for row in cur:
                    rows.append(row)
                    arinv_id = row[0]
                    booking_id = row[1]
                    booking_date = row[2]
                    booking_time = row[3]
                    guest_name = row[4]
                    therapist = row[5]

                    data.append({
                        str("arinv_id"):str(arinv_id), str("bk_id"):str(booking_id),
                        str("bk_date"):str(booking_date), str("bk_time"):str(booking_time),
                        str("guest"):str(guest_name), str("therapist"):str(therapist)
                    })

                result = {responseCode:"200", responseText:"Success", responseList:data}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result