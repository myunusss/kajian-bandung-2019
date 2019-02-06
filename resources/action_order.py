from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

class AcceptOrder(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set accept_order_time = current_timestamp " +
                "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)", [arinvoice_id, username])

                # UPDATE ROOM STATUS OCCUPIED (3)
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [3, arinvoice_id])

                # UPDATE THERAPIST STATUS
                cur.execute("update therapist set therapist_status = %s "
                "where login_id = %s", [3, username])

                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class AcceptAtRoom(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""
        
        if (request.form.get("room_code") != None):
            room_code = request.form.get("room_code")
        else:
            room_code = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("select qr_code from room r " +
                "inner join arinv a on a.room_id = r.room_id " +
                "where a.arinvoice_id = %s", [arinvoice_id])
                data = cur.fetchone()[0]

                if (data == room_code):
                    cur.execute("update arinv_therapist set ready_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)", [arinvoice_id, username])

                    result = {responseCode:"200", responseText:"Success"}
                else:
                    result = {responseCode:"401", responseText:"Room Tidak Sesuai"}
                
                conn.commit()
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class GuestAtRoom(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                
                cur.execute("update arinv_therapist set guest_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)", [arinvoice_id, username])

                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class BeginTreatment(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set begin_treatment_time = current_timestamp, " +
                "must_end_treatment_time = (select current_timestamp + interval '1h' * " +
                "(SELECT sum(COALESCE(item.duration::integer, 0)::numeric * ai.quantity / 60) AS sum " +
                    "FROM arinv_item ai " +
                    "JOIN item ON ai.item_id = item.item_id " +
                    "LEFT JOIN arinv ar ON ar.arinvoice_id = ai.arinvoice_id " +
                    "WHERE ai.arinvoice_id = %s AND item.item_group_id = 1) " +
                    "from arinv_therapist " +
                    "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)) " +
                "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)", [arinvoice_id, arinvoice_id, username, arinvoice_id, username])

                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class EndTreatment(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set end_treatment_time = current_timestamp " +
                "where arinvoice_id = %s and therapist_id in (select therapist_id from therapist where login_id = %s)", [arinvoice_id, username])

                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class LeaveRoom(Resource):
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

        if (request.form.get("arinvoice_id") != None):
            arinvoice_id = request.form.get("arinvoice_id")
        else:
            arinvoice_id = ""

        try:
            conn, cur = ConnectDB()
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [4, arinvoice_id])

                # UPDATE THERAPIST STATUS
                cur.execute("update therapist set therapist_status = %s "
                "where login_id = %s", [2, username])

                conn.commit()

                result = {responseCode:"200", responseText:"Success"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result