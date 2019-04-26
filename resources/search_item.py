from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.rupiah import rupiah_format
from common.app_setting import responseCode, responseList, responseText, detail

app = Flask(__name__)

class SearchItem(Resource):
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

        if (request.form.get("query") != None):
            query = request.form.get("query")
        else:
            query = ""

        if (request.form.get("arinv_id") != None):
            arinv_id = request.form.get("arinv_id")
        else:
            arinv_id = ""
        
        query = '%' + query + '%'

        conn, cur = ConnectDB()
        try:
            if (username != "" and session_token != "" and device_id != ""):
                cur.execute("select item.item_id, item.item_name, pi.unit_price from item " +
                "inner join arinv a on a.arinvoice_id = %s " +
                "inner join customer c on a.customer_id = c.customer_id " +
                "inner join pricelist_item pi on item.item_id = pi.item_id " +
                "where c.pricelist_id = pi.pricelist_id and item.item_name like UPPER(%s) " +
                "and item.item_group_id = 2 order by item.item_name", [arinv_id, query])

                rows = []
                data = []

                for row in cur:
                    rows.append(row)
                    item_id = row[0]
                    item_name = row[1]
                    unit_price = rupiah_format(row[2])

                    data.append({
                        str("it_id"):str(item_id), str("it_name"):str(item_name),
                        str("it_price"):str(unit_price), str("qty"):1,
                        str("note"):str('')
                        })

                result = {responseCode:"200", responseText:"Success", responseList:data}
            else:
                result = {responseCode:"401", responseText:"Not valid token"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}

        finally:
            CloseDB(conn, cur)

        return result