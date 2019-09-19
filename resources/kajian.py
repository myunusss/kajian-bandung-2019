from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id, tanggal, deskripsi, pemateri, poster_path

class Kajian(Resource):
  def post(self):
    if (request.form.get("date") != None):
        date = request.form.get("date")
    else:
        date = ""

    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_kajian, tanggal, deskripsi, nama_pemateri, poster_path " +
            "from kajian " +
            "inner join kajian_pemateri using (id_kajian) " +
            "inner join kajian_poster using (id_kajian) " +
            "inner join pemateri using (id_pemateri) " +
            "where date(tanggal) = %s", [date])
            
            data = []

            for row in cur:
                v_id = row[0]
                v_tanggal = row[1]
                v_deskripsi = row[2]
                v_pemateri = row[3]
                v_poster_path = row[4]

                data.append({
                    _id:str(v_id),
                    tanggal:str(v_tanggal),
                    deskripsi:str(v_deskripsi),
                    pemateri:str(v_pemateri),
                    poster_path:str(v_poster_path)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class ListKajian(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            FMT_1 = '%Y'
            year = str(datetime.now().strftime(FMT_1))
            FMT_2 = '%m'
            month = str(datetime.now().strftime(FMT_2))

            cur.execute("select distinct(date(tanggal)) " + 
            "from kajian " +
            "where extract(year from tanggal) = %s and extract(month from tanggal) = %s", [year, month])
            data = []
            for row in cur:
                v_tanggal = row[0]

                data.append({
                    tanggal:str(v_tanggal)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result