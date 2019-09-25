from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id, deskripsi, poster_path, tanggal

class QuoteToday(Resource):
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

            cur.execute("select id_quote, poster_path, deskripsi, tanggal from quote where date(tanggal) = %s limit 1", [date_now])
            val = cur.fetchone()
            
            if (val != None):
                v_id = val[0]
                v_poster_path = val[1]
                v_deskripsi = val[2]
                v_tanggal = val[3]

            result = {responseCode:"200", responseText:"success", poster_path:v_poster_path}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class AllQuote(Resource):
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

            cur.execute("select id_quote, poster_path, tanggal, deskripsi from quote")
            data = []
            for row in cur:
                v_id = row[0]
                v_poster_path = row[1]
                v_tanggal = row[2]
                v_deskripsi = row[3]

                data.append({
                    _id:str(v_id),
                    poster_path:str(v_poster_path),
                    tanggal:str(v_tanggal),
                    deskripsi:str(v_deskripsi)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result