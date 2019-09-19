from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseList, responseText, detail, _id, nama, deskripsi, ig_akun, poster_path

class Kolaborasi(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_kolaborasi, nama, poster_path, deskripsi, ig_akun from kolaborasi")
            data = []
            for row in cur:
                v_id = row[0]
                v_nama = row[1]
                v_poster_path = row[2]
                v_deskripsi = row[3]
                v_ig_akun = row[4]

                data.append({
                    _id:str(v_id),
                    nama:str(v_nama),
                    poster_path:str(v_poster_path),
                    deskripsi:str(v_deskripsi),
                    ig_akun:str(v_ig_akun)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result