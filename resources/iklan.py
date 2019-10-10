from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id, deskripsi, poster_path, from_date, to_date

class Iklan(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            FMT_1 = '%Y-%m-%d'
            date_now = str(datetime.now().strftime(FMT_1))

            cur.execute("select id_iklan, poster_path, deskripsi, from_date, to_date from iklan where date(to_date) >= %s and aktif = 1", [date_now])
            data = []
            for row in cur:
                v_id = row[0]
                v_poster_path = row[1]
                v_deskripsi = row[2]
                v_from_date = row[3]
                v_to_date = row[4]

                data.append({
                    _id:str(v_id),
                    poster_path:str(v_poster_path),
                    deskripsi:str(v_deskripsi),
                    from_date:str(v_from_date),
                    to_date:str(v_to_date)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class NewInfo(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):

            cur.execute("select pesan, aktif from info where aktif = 1 limit 1")
            row = cur.fetchone()

            if (row != None):
                v_pesan = row[0]
                v_aktif = row[1]

            result = {
                responseCode:"200",
                responseText:"success",
                "pesan":str(v_pesan),
                "aktif":str(v_aktif)
            }
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result