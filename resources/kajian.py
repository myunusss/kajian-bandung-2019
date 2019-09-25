from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id, tanggal, deskripsi, pemateri, poster_path, bulan, hari, full_date, tempat, judul, resume

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

class DetailKajian(Resource):
  def post(self):
    if (request.form.get("id_kajian") != None):
        id_kajian = request.form.get("id_kajian")
    else:
        id_kajian = ""

    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_kajian, tanggal, deskripsi, nama_pemateri, poster_path, tempat, judul, p.panggilan " +
            "from kajian " +
            "inner join kajian_pemateri using (id_kajian) " +
            "inner join kajian_poster using (id_kajian) " +
            "inner join pemateri p using (id_pemateri) " +
            "where id_kajian = %s", [id_kajian])
            
            row = cur.fetchone()

            if (row != None):
                v_id = row[0]
                v_tanggal = row[1]
                v_deskripsi = row[2]
                v_poster_path = row[4]
                v_tempat = row[5]
                v_judul = row[6]
                v_pemateri = row[7] + ' ' + row[3]

                result = {responseCode:"200", responseText:"success", _id:str(v_id), tanggal:str(v_tanggal), deskripsi:v_deskripsi, poster_path:v_poster_path, tempat:v_tempat, judul:v_judul, pemateri:str(v_pemateri)}
            else:
                result = {responseCode:"401", responseText:"Not found"}
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
            now = datetime.now()
            FMT_1 = '%Y'
            year = str(now.strftime(FMT_1))
            FMT_2 = '%m'
            month = str(now.strftime(FMT_2))
            day_name = str(now.strftime("%A"))
            month_name = str(now.strftime("%B"))

            cur.execute("select distinct(date_part('day', tanggal)) as day_, date(tanggal) as full_date " + 
            "from kajian " +
            "where extract(year from tanggal) = %s and extract(month from tanggal) = %s", [year, month])
            data = []
            for row in cur:
                v_tanggal = row[0]
                v_full_date = row[1]

                data.append({
                    bulan: month_name,
                    tanggal: str(int(v_tanggal)),
                    full_date: str(v_full_date)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class Resume(Resource):
  def post(self):
    if (request.form.get("id_kajian") != None):
        id_kajian = request.form.get("id_kajian")
    else:
        id_kajian = ""

    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            now = datetime.now()
            FMT_1 = '%Y'
            year = str(now.strftime(FMT_1))
            FMT_2 = '%m'
            month = str(now.strftime(FMT_2))

            cur.execute("select id_kajian, tanggal, deskripsi, nama_pemateri, poster_path, tempat, judul, p.panggilan, resume " +
            "from kajian " +
            "inner join kajian_pemateri using (id_kajian) " +
            "inner join kajian_poster using (id_kajian) " +
            "inner join pemateri p using (id_pemateri) " +
            "where resume is not null and extract(year from tanggal) = %s and extract(month from tanggal) = %s", [year, month])

            data = []
            
            for row in cur:
                v_id = row[0]
                v_tanggal = row[1]
                v_deskripsi = row[2]
                v_poster_path = row[4]
                v_tempat = row[5]
                v_judul = row[6]
                v_pemateri = row[7] + ' ' + row[3]
                v_resume = row[8]

                data.append({
                    _id: str(v_id),
                    tanggal: str(v_tanggal),
                    deskripsi: v_deskripsi,
                    poster_path: v_poster_path,
                    tempat: v_tempat,
                    judul: v_judul,
                    pemateri: v_pemateri,
                    resume: v_resume
                })

                result = {responseCode:"200", responseText:"success", responseList:data}
            else:
                result = {responseCode:"401", responseText:"Not found"}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result