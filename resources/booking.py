from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

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

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                
                cur.execute("SELECT booking.booking_id, booking.booking_date, " +
                "to_char(booking.booking_time::interval, 'HH24:MI'::text) AS booking_time, booking.guest_name, " +
                "bt.therapist_id " +
                "FROM booking " +
                "inner join booking_therapist bt on booking.booking_id = bt.booking_id " +
                "WHERE booking.booking_date = 'now'::text::date " +
                    "and bt.therapist_id in (select therapist_id from therapist where login_id = %s) " +
                "ORDER BY booking.booking_date, to_char(booking.booking_time::interval, 'HH24:MI'::text);", [username])

                rows = []
                data = []

                for row in cur:
                    rows.append(row)
                    booking_id = row[0]
                    booking_date = row[1]
                    booking_time = row[2]
                    guest_name = row[3]
                    therapist = row[4]

                    data.append({
                        str("bk_id"):str(booking_id), str("bk_date"):str(booking_date), str("bk_time"):str(booking_time),
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