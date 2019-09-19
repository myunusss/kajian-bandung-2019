from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseList, responseText, detail, _id, nama, deskripsi, ig_akun, poster_path

class Kolaborasi(Resource):
  def get(self):
    conn, cur = ConnectDB()
    try:
        cur.execute("select id_kolaborasi, nama, poster_path, deskripsi, ig_akun from kolaborasi")
        data = []
        for row in cur:
            v_id = row[0]
            v_nama = row[1]
            v_poster_path = row[2]
            v_deskripsi = row[2]
            v_ig_akun = row[3]

            data.append({
                _id:str(v_id),
                nama:str(v_nama),
                poster_path:str(v_poster_path),
                deskripsi:str(v_deskripsi),
                ig_akun:str(v_ig_akun)
            })

        result = {responseCode:"200", responseText:"success", responseList:data}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result