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

        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = ""

        conn, cur = ConnectDB()

        try:
            cur.execute("update arinv_therapist set accept_order_time = current_timestamp " +
            "where arinvoice_id = %s and therapist_id = %s", [arinvoice_id, ther_id])

            count = cur.rowcount

            # UPDATE THERAPIST STATUS
            cur.execute("update therapist set therapist_status = %s "
            "where therapist_id = %s", [3, ther_id])

            count = count + cur.rowcount

            # UPDATE ROOM STATUS OCCUPIED (3)
            cur.execute("update room set room_status_id = %s " +
            "where room_id in (select room_id from arinv where arinvoice_id = %s)", [3, arinvoice_id])

            count = count + cur.rowcount

            if (count > 2):
                conn.commit()
                result = {responseCode:"200", responseText:"Success"}
            else :
                conn.rollback()
                result = {responseCode:"401", responseText:"Failed update data, please try again"}
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

        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = ""

        conn, cur = ConnectDB()
        try:
            if (ther_id != "" and username != "" and session_token != "" and device_id != ""):
                cur.execute("select qr_code from room r " +
                "inner join arinv a on a.room_id = r.room_id " +
                "where a.arinvoice_id = %s", [arinvoice_id])
                data = cur.fetchone()[0]

                if (data == room_code):
                    title = 'Order Info'
                    messageReady = username + " ready at room"
                    module = 'Therapist'
                    ch_id = 'cso_info'

                    cur.execute("update arinv_therapist set ready_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s and therapist_id = %s", [arinvoice_id, ther_id])

                    count = cur.rowcount

                    # SEND NOTIF KE CSO
                    cur.execute("select fcm_client_token from salesman " +
                        "inner join cso_session using (salesman_id)"
                        "where coalesce(disabled, 0) != 1 and fcm_client_token is not null order by login_time desc limit 1")
                    v_data = cur.fetchall()

                    for _data in v_data:
                        c_token = _data[0]

                        cur.execute("insert into fcm_notif (fcm_client_token, title, message, module, entry_time, rel_entity_id, sent, channel_id) " +
                            "values (%s, %s, %s, %s, current_timestamp, %s, 0, %s)", [c_token, title, messageReady, module, ther_id, ch_id])

                    if (count != 0):
                        conn.commit()
                        result = {responseCode:"200", responseText:"Success"}
                    else :
                        conn.rollback()
                        result = {responseCode:"401", responseText:"Failed update data, please try again"}
                else:
                    result = {responseCode:"401", responseText:"Room Tidak Sesuai"}
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

        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = ""

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                
                cur.execute("update arinv_therapist set guest_at_room_time = current_timestamp " +
                    "where arinvoice_id = %s", [arinvoice_id])
                
                count = cur.rowcount

                if (count != 0):
                    conn.commit()
                    result = {responseCode:"200", responseText:"Success"}
                else :
                    conn.rollback()
                    result = {responseCode:"401", responseText:"Failed update data, please try again"}
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

        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = ""

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
                    "where arinvoice_id = %s and therapist_id = %s) " +
                "where arinvoice_id = %s", [arinvoice_id, arinvoice_id, ther_id, arinvoice_id])

                count = cur.rowcount

                # UPDATE ROOM STATUS OCCUPIED (3)
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [3, arinvoice_id])

                count = count + cur.rowcount
    # insert log
                myActions = "Begin Treatment by Therapist - " + username
                cur.execute("insert into log_treatment (arinvoice_id, log_time, action) " +
                "values (%s, current_timestamp, %s)", [arinvoice_id, myActions])

                if (count > 1):
                    conn.commit()
                    result = {responseCode:"200", responseText:"Success"}
                else :
                    conn.rollback()
                    result = {responseCode:"401", responseText:"Failed update data, please try again"}
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
        
        if (request.form.get("ther_id") != None):
            ther_id = request.form.get("ther_id")
        else:
            ther_id = 0

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("update arinv_therapist set end_treatment_time = current_timestamp " +
                "where arinvoice_id = %s and end_treatment_time is null", [arinvoice_id])
                
                count = cur.rowcount

                # UPDATE ROOM STATUS KE DIRTY
                cur.execute("update room set room_status_id = %s " +
                "where room_id in (select room_id from arinv where arinvoice_id = %s)", [4, arinvoice_id])

                count = count + cur.rowcount

                # UPDATE THERAPIST STATUS
                cur.execute("update therapist set therapist_status = %s "
                "where therapist_id in (select therapist_id from arinv_therapist where arinvoice_id = %s)", [1, arinvoice_id])

                count = count + cur.rowcount

                # insert log
                myActions = "End Treatment by Therapist - " + username
                cur.execute("insert into log_treatment (arinvoice_id, log_time, action) " +
                "values (%s, current_timestamp, %s)", [arinvoice_id, myActions])

                # SEND NOTIF KE CSO
                cur.execute("select fcm_client_token from salesman " +
                        "inner join cso_session using (salesman_id)"
                        "where coalesce(disabled, 0) != 1 and fcm_client_token is not null order by login_time desc limit 1")
                v_data = cur.fetchall()

                title = 'Info'
                messageEnd = username + " menyelesaikan treatment"
                module = 'Therapist'
                ch_id = 'cso_info'

                for _data in v_data:
                    c_token = _data[0]

                    cur.execute("insert into fcm_notif (fcm_client_token, title, message, module, entry_time, rel_entity_id, sent, channel_id) " +
                        "values (%s, %s, %s, %s, current_timestamp, %s, 0, %s)", [c_token, title, messageEnd, module, ther_id, ch_id])

                if (count > 2):
                    conn.commit()
                    result = {responseCode:"200", responseText:"Success"}
                else :
                    conn.rollback()
                    result = {responseCode:"401", responseText:"Failed update data, please try again"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result