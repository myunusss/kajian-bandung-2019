from flask import Flask, request, json
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.rupiah import rupiah_format

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

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

        print("addnewitem", request.form)

        items = json.loads(items)

        print("ITEMS", items)

        try:
            conn, cur = ConnectDB()
            
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

                # INSERT TO ARINV ITEM
                cur.execute("insert into arinv_item (arinvoice_id, seq, item_id, quantity, unit_price, order_status, description) " +
                "values (%s, %s, %s, %s, %s, %s, %s)", [arinv_id, seq, item_id, qty, unit_price, 0, note])

            # FUNCTION TO UPDATE PRICE ALL
            cur.execute("select update_price_all(%s)", [arinv_id])

            conn.commit()

            result = {responseCode:"200", responseText:"Success"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result
