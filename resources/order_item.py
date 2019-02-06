from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.rupiah import rupiah_format

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
dataStatus="data_status"
detail="detail"

class OrderListItem(Resource):
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
                
                cur.execute("select a.arinvoice_id from arinv a " +
                "inner join arinv_therapist at on at.arinvoice_id = a.arinvoice_id " +
                "where therapist_id in (select therapist_id from therapist where login_id = %s) and posted = 0 and end_treatment_time is null " +
                "order by invoice_time limit 1", [username])

                row = cur.fetchone()

                if (row != None):
                    arinvoice_id = row[0]
                    print("invoice id", arinvoice_id)

                    cur.execute("select * from get_price_item_by_pricelist(%s)", [arinvoice_id])

                    rows = []
                    data = []

                    for row in cur:
                        rows.append(row)
                        item_name = row[0]
                        quantity = row[1]
                        unit_price = rupiah_format(row[2])
                        amount = rupiah_format(row[4])

                        data.append({
                            str("arinv_id"):str(arinvoice_id), str("qty"):str(quantity),
                            str("name"):str(item_name), str("price"):str(unit_price),
                            str("amount"):str(amount)
                        })
                    
                    cur.execute("select total_price_item from arinv where arinvoice_id = %s", [arinvoice_id])

                    total = cur.fetchone()[0]
                    print("total", total)

                    result = {responseCode:"200", responseText:"Success", responseList:data, "total":rupiah_format(total)}
                else :
                    result = {responseCode:"200", responseText:"Success", dataStatus:"null"}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result