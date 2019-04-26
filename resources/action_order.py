from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail

app = Flask(__name__)

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

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set accept_order_time = current_timestamp " +
                "where arinvoice_id = %s and therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                "and logout_time is null)", [arinvoice_id, session_token])

                # UPDATE ROOM STATUS OCCUPIED (3)
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [3, arinvoice_id])

                # UPDATE THERAPIST STATUS
                cur.execute("update therapist set therapist_status = %s "
                "where therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                "and logout_time is null)", [3, session_token])

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

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("select qr_code from room r " +
                "inner join arinv a on a.room_id = r.room_id " +
                "where a.arinvoice_id = %s", [arinvoice_id])
                data = cur.fetchone()[0]

                if (data == room_code):
                    cur.execute("update arinv_therapist set ready_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s and therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                    "and logout_time is null)", [arinvoice_id, session_token])

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

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                
                cur.execute("update arinv_therapist set guest_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s", [arinvoice_id])

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

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set begin_treatment_time = current_timestamp, " +
                "must_end_treatment_time = (select current_timestamp + interval '1h' * " +
                "(SELECT sum(COALESCE(item.duration::integer, 0)::numeric * ai.quantity / 60) AS sum " +
                    "FROM arinv_item ai " +
                    "JOIN item ON ai.item_id = item.item_id " +
                    "LEFT JOIN arinv ar ON ar.arinvoice_id = ai.arinvoice_id " +
                    "WHERE ai.arinvoice_id = %s AND item.item_group_id = 1) " +
                    "from arinv_therapist " +
                    "where arinvoice_id = %s and therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                    "and logout_time is null)) " +
                "where arinvoice_id = %s", [arinvoice_id, arinvoice_id, session_token, arinvoice_id])

                # UPDATE ROOM STATUS OCCUPIED (3)
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [3, arinvoice_id])

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

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set end_treatment_time = current_timestamp " +
                "where arinvoice_id = %s and end_treatment_time is null", [arinvoice_id])

                # UPDATE ROOM STATUS KE DIRTY
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s) and room_status_id = 3", [4, arinvoice_id])

                # UPDATE THERAPIST STATUS
                cur.execute("update therapist set therapist_status = %s "
                "where therapist_id in (select therapist_id from arinv_therapist where arinvoice_id = %s) and therapist_status = 3", [1, arinvoice_id])

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