from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail

app = Flask(__name__)

data="data"

class GetRecentOrder(Resource):
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
                
                cur.execute("select * from get_recent_order(%s,'recent')", [session_token])

                row = cur.fetchone()
                if (row != None):
                    invoice_time = row[0]
                    card_no = row[1]
                    room_no = row[2]
                    therapists = row[3]
                    begin_time = row[4]
                    end_time = row[5]
                    item_name = row[6]
                    class_id = row[7]
                    arinv_id = row[8]
                    must_end_time = row[9]

                    if (must_end_time != None):
                        FMT = '%Y-%m-%d %H:%M:%S'
                        now = str(datetime.now().strftime(FMT))
                        remaining_time = datetime.strptime(must_end_time, FMT) - datetime.strptime(now, FMT)
                        total_sec = remaining_time.total_seconds()

                        if (total_sec <= 0):
                            total_sec = 0
                    else:
                        must_end_time = '-'
                        total_sec = '-'

                    # FMT = '%H:%M:%S'
                    # now = str(datetime.now().strftime('%H:%M:%S'))
                    # remaining_time = datetime.strptime(must_end_time, FMT) - datetime.strptime(now, FMT)
                    # total_sec = remaining_time.total_seconds()

                    cur.execute("select * from get_recent_order_status(%s, %s)", [0, arinv_id])
                    status_order = cur.fetchone()[0]

                    if (status_order >= 1):
                        new_ther_stat = 3
                    else :
                        new_ther_stat = 1
                    
                    cur.execute("update therapist set therapist_status = %s " +
                        "where therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                        "and logout_time is null)", [new_ther_stat, session_token])

                    conn.commit()

                    result = {
                        responseCode:"200", responseText:"Success", data:"notNull", str("arinv_id"):str(arinv_id),
                        str("invoice_time"):str(invoice_time), str("status_order"):str(status_order),
                        str("card_no"):str(card_no), str("room_no"):str(room_no),
                        str("therapists"):str(therapists), str("begin_time"):str(begin_time),
                        str("end_time"):str(end_time), str("item_name"):str(item_name), str("class_id"):str(class_id),
                        str("remaining_time"):str(total_sec), str("must_end_time"):str(must_end_time)
                    }
                else:
                    result = {
                        responseCode:"200", responseText:"Data Kosong", data:"null"
                    }
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result

class NextOrder(Resource):
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
                cur.execute("select * from get_recent_order(%s,'')", [session_token])
                # select from function
                data = []
                for row in cur:
                    invoice_time = row[0]
                    card_no = row[1]
                    room_no = row[2]
                    therapists = row[3]
                    begin_time = row[4]
                    end_time = row[5]
                    item_name = row[6]
                    class_id = row[7]
                    arinv_id = row[8]

                    data.append({
                        str("arinv_id"):str(arinv_id), str("invoice_time"):str(invoice_time),
                        str("card_no"):str(card_no), str("room_no"):str(room_no),
                        str("therapists"):str(therapists), str("begin_time"):str(begin_time),
                        str("end_time"):str(end_time), str("item_name"):str(item_name), str("class_id"):str(class_id)
                    })
                
                result = {responseCode:"200", responseText:"Success", responseList:data}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result


# TIDAK DIPAKAI *identik dengan get recent order, TAPI SIMPAN DULU
class DetailOrder(Resource):
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
                cur.execute("select * from get_recent_order(%s,'recent')", [session_token])
                
                # cur.execute("SELECT to_char(a.invoice_time, 'HH24:MI'::text) AS invoice_time,  (g.card_no || ' - ' || a.guest_name) as guest, " +
                # "(r.room_no || ' - ' || rt.type_name)::varchar(100), " +
                # "array_to_string(ARRAY( SELECT therapist.therapist_name " +
                # "FROM arinv_therapist at JOIN therapist ON at.therapist_id = therapist.therapist_id " +
                # "WHERE a.arinvoice_id = at.arinvoice_id " +
                # "ORDER BY therapist.therapist_name), ', '::text)::character varying(200) AS therapists, " +
                # "case when begin_treatment_time is not null then to_char(art.begin_treatment_time, 'HH24:MI:SS'::text) else '-' end AS begin_time, " +
                # "case when end_treatment_time is not null then to_char(art.end_treatment_time, 'HH24:MI:SS'::text) else '-' end AS end_time, " +
                # "i.item_name, t.class_id, a.arinvoice_id, " +
                # "case when must_end_treatment_time is not null then to_char(art.must_end_treatment_time, 'YYYY-MM-DD HH24:MI:SS'::text) else '0000-00-00 00:00:00' end AS must_end_time " +
                # "FROM arinv a " +
                # "left join gcard g ON g.gcard_id = a.gcard_id " +
                # "left join room r ON r.room_id = a.room_id " +
                # "left join room_type rt on r.room_type_id = rt.room_type_id " +
                # "left JOIN arinv_therapist art ON a.arinvoice_id = art.arinvoice_id " +
                # "left JOIN therapist t ON t.therapist_id = art.therapist_id " +
                # "left JOIN item i ON a.treatment_item_id = i.item_id " +
                # "WHERE a.arinvoice_id = %s and art.therapist_id in (select therapist_id from ther_session where user_token = %s " + 
                # "and logout_time is null) " +
                # "GROUP BY g.card_no, r.room_no, art.begin_treatment_time, art.end_treatment_time, i.item_name, t.class_id, a.arinvoice_id, rt.type_name, " +
                # "therapists, a.invoice_time, art.must_end_treatment_time", [arinvoice_id, session_token])

                row = cur.fetchone()
                if (row != None):
                    invoice_time = row[0]
                    card_no = row[1]
                    room_no = row[2]
                    therapists = row[3]
                    begin_time = row[4]
                    end_time = row[5]
                    item_name = row[6]
                    class_id = row[7]
                    arinv_id = row[8]
                    must_end_time = row[9]
                    
                    FMT = '%Y-%m-%d %H:%M:%S'
                    now = str(datetime.now().strftime(FMT))
                    remaining_time = datetime.strptime(must_end_time, FMT) - datetime.strptime(now, FMT)
                    total_sec = remaining_time.total_seconds()

                    result = {
                        responseCode:"200", responseText:"Success", str("arinv_id"):str(arinv_id),
                        str("invoice_time"):str(invoice_time),
                        str("card_no"):str(card_no), str("room_no"):str(room_no),
                        str("therapists"):str(therapists), str("begin_time"):str(begin_time),
                        str("end_time"):str(end_time), str("item_name"):str(item_name), str("class_id"):str(class_id),
                        str("remaining_time"):str(total_sec), str("must_end_time"):str(must_end_time)
                    }
                    
                else:
                    result = {
                        responseCode:"404", responseText:"Data Kosong"
                    }
            else:
                result = {responseCode:"401", responseText:"Not valid token"}
                
        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)
        
        # print(result)

        return result
