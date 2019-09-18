from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseList, responseText, detail

class Kajian(Resource):
  def get(self):
    conn, cur = ConnectDB()    
    try:
        cur.execute("select id_kajian, tanggal, deskripsi from kajian")
        data = []
        for row in cur:
            v_id = row[0]
            v_tanggal = row[1]
            v_deskripsi = row[2]

            data.append({
                str("id"):str(v_id),
                str("tanggal"):str(v_tanggal),
                str("deskripsi"):str(v_deskripsi)
            })

        result = {responseCode:"200", responseText:"success", responseList:data}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result