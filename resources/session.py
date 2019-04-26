from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail

app = Flask(__name__)

class AddSession(Resource):
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

        if (request.form.get("arinv_id") != None):
            arinv_id = request.form.get("arinv_id")
        else:
            arinv_id = ""

        if (request.form.get("qty") != None):
            quantity = request.form.get("qty")
        else:
            quantity = ""

        conn, cur = ConnectDB()
        try:
            seq = 1
            # GET SEQUENCE FROM ARINV ITEM
            cur.execute("select max(seq) from arinv_item where arinvoice_id = %s", [arinv_id])
            max_seq = cur.fetchone()[0]
            if max_seq != None:
                seq = max_seq + 1

            cur.execute("select coalesce(unit_price, 0) as unit_price, item_id " +
            "from pricelist_item pi " +
            "inner join customer c on c.pricelist_id = pi.pricelist_id " +
            "where customer_id in (select customer_id from arinv where arinvoice_id = %s) " +
            "and item_id in (select i.item_id from item i " +
            "where parent_item_id in (select treatment_item_id from arinv where arinvoice_id = %s))", [arinv_id, arinv_id])
            
            row = cur.fetchone()
            unit_price = row[0]
            item_id = row[1]

            cur.execute("insert into arinv_item (arinvoice_id, seq, item_id, quantity, unit_price, order_status) values (%s, %s, %s, %s, %s, %s)", [arinv_id, seq, item_id, quantity, unit_price, 1])

            cur.execute('select item_group_id from item where item_id = %s',[item_id])
            item_group = cur.fetchone()[0]

            # UPDATE MUST END TREATMENT TIME * 60 karena dirubah ke jam
            cur.execute("update arinv_therapist set " +
		    "must_end_treatment_time = (select begin_treatment_time + interval '1h' * " +
            "(select sum(coalesce(duration::integer, 0)::numeric * ai.quantity / 60) as sum from arinv_item ai " +
			"join item using(item_id) where item.item_group_id = %s and ai.arinvoice_id = %s) from arinv_therapist " +
			"where arinvoice_id = %s) where arinvoice_id = %s", [item_group, arinv_id, arinv_id, arinv_id])

            # cur.execute("update arinv_therapist set " +
            #     "must_end_treatment_time = (select must_end_treatment_time + interval '1h' * "
            #     "(select sum(coalesce(duration::integer, 0)::numeric / 60) as sum from item where item_id = %s)) "
            #     "where arinvoice_id = %s", [item_id, arinv_id])

            # FUNCTION TO UPDATE PRICE ALL
            cur.execute("select update_price_all(%s)", [arinv_id])

            conn.commit()

            result = {responseCode:"200", responseText:"Success"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result