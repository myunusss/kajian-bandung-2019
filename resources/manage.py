from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id, aktif, tanggal, poster_path, deskripsi, from_date, to_date, nama, panggilan, ig_akun

class AddKajian(Resource):
  def post(self):
    
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    if (request.form.get("judul") != None):
        judul = request.form.get("judul")
    else:
        judul = ""

    if (request.form.get("tempat") != None):
        tempat = request.form.get("tempat")
    else:
        tempat = ""
    
    if (request.form.get("waktu") != None):
        waktu = request.form.get("waktu")
    else:
        waktu = ""

    if (request.form.get("geo") != None):
        geo = request.form.get("geo")
    else:
        geo = ""

    if (request.form.get("deskripsi") != None):
        deskripsi = request.form.get("deskripsi")
    else:
        deskripsi = ""

    if (request.form.get("id_pemateri") != None):
        id_pemateri = request.form.get("id_pemateri")
    else:
        id_pemateri = ""

    if (request.form.get("poster_path") != None):
        poster_path = request.form.get("poster_path")
    else:
        poster_path = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("insert into kajian (tanggal, judul, tempat, geo, deskripsi) values (%s, %s, %s, %s, %s) RETURNING id_kajian", [waktu, judul, tempat, geo, deskripsi])
            id_kajian = cur.fetchone()[0]

            if (id_kajian != None):
                cur.execute("insert into kajian_pemateri (id_kajian, id_pemateri) values (%s, %s)", [id_kajian, id_pemateri])
                cur.execute("insert into kajian_poster (id_kajian, poster_path) values (%s, %s)", [id_kajian, poster_path])

                conn.commit()
                result = {responseCode:"200", responseText:"success", _id:str(id_kajian)}
            else:
                result = {responseCode:"401", responseText:"Please try again"}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}

    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
        conn.rollback()
    finally:
        CloseDB(conn, cur)
    return result

class AddPemateri(Resource):
  def post(self):
    
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    if (request.form.get("panggilan") != None):
        panggilan = request.form.get("panggilan")
    else:
        panggilan = ""

    if (request.form.get("nama_pemateri") != None):
        nama_pemateri = request.form.get("nama_pemateri")
    else:
        nama_pemateri = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("insert into pemateri (nama_pemateri, panggilan) values (%s, %s) RETURNING id_pemateri", [nama_pemateri, panggilan])
            id_pemateri = cur.fetchone()[0]

            if (id_pemateri != None):
                conn.commit()
                result = {responseCode:"200", responseText:"success", _id:str(id_pemateri)}
            else:
                result = {responseCode:"401", responseText:"Please try again"}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}

    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
        conn.rollback()
    finally:
        CloseDB(conn, cur)
    return result

class AddInfo(Resource):
  def post(self):
    
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    if (request.form.get("pesan") != None):
        pesan = request.form.get("pesan")
    else:
        pesan = ""

    if (request.form.get("aktif") != None):
        aktif = request.form.get("aktif")
    else:
        aktif = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("insert into info (pesan, aktif) values (%s, %s) RETURNING id_info", [pesan, aktif])
            id_info = cur.fetchone()[0]

            if (id_info != None):
                conn.commit()
                result = {responseCode:"200", responseText:"success", _id:str(id_info)}
            else:
                result = {responseCode:"401", responseText:"Please try again"}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}

    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
        conn.rollback()
    finally:
        CloseDB(conn, cur)
    return result

class UpdateInfo(Resource):
  def post(self):
    
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    if (request.form.get("id_pesan") != None):
        id_pesan = request.form.get("id_pesan")
    else:
        id_pesan = ""

    if (request.form.get("aktif") != None):
        aktif = request.form.get("aktif")
    else:
        aktif = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("update info set aktif = %s where id_pesan = %s ", [aktif, id_pesan])
            cur.execute("update info set aktif = %s where id_pesan != %s ", [0, id_pesan])
            conn.commit()
            result = {responseCode:"200", responseText:"success", _id:str(id_pesan)}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}

    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
        conn.rollback()
    finally:
        CloseDB(conn, cur)
    return result

class AllIklan(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_iklan, poster_path, deskripsi, from_date, to_date, aktif from iklan")
            data = []
            for row in cur:
                v_id = row[0]
                v_poster_path = row[1]
                v_deskripsi = row[2]
                v_from_date = row[3]
                v_to_date = row[4]
                v_aktif = row[5]

                data.append({
                    _id:str(v_id),
                    poster_path:str(v_poster_path),
                    deskripsi:str(v_deskripsi),
                    from_date:str(v_from_date),
                    to_date:str(v_to_date),
                    aktif:str(v_aktif)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class AllPemateri(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_pemateri, nama_pemateri, panggilan from pemateri")
            data = []
            for row in cur:
                v_id = row[0]
                v_nama = row[1]
                v_panggilan = row[2]

                data.append({
                    _id:str(v_id),
                    nama:str(v_nama),
                    panggilan:str(v_panggilan)
                })

            result = {responseCode:"200", responseText:"success", responseList:data}
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}
    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result

class AllKolaborasi(Resource):
  def post(self):
    if (request.form.get("session_token") != None):
        session_token = request.form.get("session_token")
    else:
        session_token = ""

    conn, cur = ConnectDB()
    try:
        if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
            cur.execute("select id_kolaborasi, aktif, nama, poster_path, deskripsi, ig_akun from kolaborasi")
            data = []
            for row in cur:
                v_id = row[0]
                v_aktif = row[1]
                v_nama = row[2]
                v_poster_path = row[3]
                v_deskripsi = row[4]
                v_ig_akun = row[5]

                data.append({
                    _id:str(v_id),
                    aktif:str(v_aktif),
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