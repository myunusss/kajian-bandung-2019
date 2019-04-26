from flask import Flask, request, json
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.rupiah import rupiah_format
from common.app_setting import responseCode, responseText, detail

app = Flask(__name__)

class AddNewItem(Resource):
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

        if (request.form.get("items") != None):
            items = request.form.get("items")
        else:
            items = ""

        if (request.form.get("arinv_id") != None):
            arinv_id = request.form.get("arinv_id")
        else:
            arinv_id = ""

        items = json.loads(items)

        conn, cur = ConnectDB()
        try:
            for item in items:
                item_id = item['it_id']
                qty = item['qty']
                note = item['note']

                seq = 1

                cur.execute("select max(seq) from arinv_item where arinvoice_id = %s", [arinv_id])
                max_seq = cur.fetchone()[0]
                if max_seq != None:
                    seq = max_seq + 1

                # GET UNIT PRICE
                cur.execute("select coalesce(unit_price, 0) from pricelist_item pi " +
                "inner join customer c on c.pricelist_id = pi.pricelist_id " +
                "where customer_id in (select customer_id from arinv where arinvoice_id = %s) "
                "and item_id = %s", [arinv_id, item_id])
                unit_price = cur.fetchone()[0]

                cur.execute("select therapist_id from ther_session where user_token = %s and logout_time is null", [session_token])
                ther_id = cur.fetchone()[0]
                
                # cek default order status
                cur.execute("select default_order_status from item_type it " +
                "inner join item i on i.item_type_id = it.item_type_id " +
                "where i.item_id = %s", [item_id])
                def_order_stat = cur.fetchone()[0]

                # INSERT TO ARINV ITEM
                cur.execute("insert into arinv_item (arinvoice_id, seq, item_id, quantity, unit_price, order_status, description, therapist_id) " +
                "values (%s, %s, %s, %s, %s, %s, %s, %s)", [arinv_id, seq, item_id, qty, unit_price, def_order_stat, note, ther_id])

            # FUNCTION TO UPDATE PRICE ALL
            cur.execute("select update_price_all(%s)", [arinv_id])

            conn.commit()

            result = {responseCode:"200", responseText:"Success"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result
