from flask import Flask, request
from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB
from datetime import datetime
from common.app_setting import responseCode, responseList, responseText, detail, _id

# class AddKajian(Resource):
#   def post(self):
#     if (request.form.get("session_token") != None):
#         session_token = request.form.get("session_token")
#     else:
#         session_token = ""

#     if (request.form.get("judul") != None):
#         judul = request.form.get("judul")
#     else:
#         judul = ""

#     if (request.form.get("tempat") != None):
#         tempat = request.form.get("tempat")
#     else:
#         tempat = ""

#     if (request.form.get("geo") != None):
#         geo = request.form.get("geo")
#     else:
#         geo = ""

#     if (request.form.get("deskripsi") != None):
#         deskripsi = request.form.get("deskripsi")
#     else:
#         deskripsi = ""

#     if (request.form.get("id_pemateri") != None):
#         id_pemateri = request.form.get("id_pemateri")
#     else:
#         id_pemateri = ""

#     if (request.form.get("poster_path") != None):
#         poster_path = request.form.get("poster_path")
#     else:
#         poster_path = ""

#     conn, cur = ConnectDB()
#     try:
#         now = datetime.now()

#         if (session_token == '$2y$12$/Am4ByLydvLE4ra2pvGDUOkDWYRi5XObtfqH/SWpRJAnJY8/dzDsS'):
#             cur.execute("insert into kajian (tanggal, judul, tempat, geo, deskripsi) values (%s, %s, %s, %s, %s)", [now, judul, tempat, geo, deskripsi])
#             id_kajian = cur.fetchone()[0]

#             cur.execute("insert into kajian_pemateri (id_kajian, id_pemateri) values (%s, %s)", [id_kajian, id_pemateri])
#             cur.execute("insert into kajian_poster (id_kajian, poster_path) values (%s, %s)", [id_kajian, poster_path])

#             if (id_kajian !== None):
#                 conn.commit()
#                 result = {responseCode:"200", responseText:"success", _id:str(id_kajian)}
#             else:
#                 result = {responseCode:"401", responseText:"Please try again"}    
#         else:
#             result = {responseCode:"401", responseText:"Ooppss..."}
#     except Exception as e:
#         result = {responseCode:"404", responseText:"Not found", detail:str(e)}
#     finally:
#         CloseDB(conn, cur)
#     return result

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
            cur.execute("insert into kajian (tanggal, judul, tempat, geo, deskripsi) values (current_timestamp, %s, %s, %s, %s)", [judul, tempat, geo, deskripsi])
            id_kajian = cur.fetchone()[0]
            print('INI', id_kajian)

            # cur.execute("insert into kajian_pemateri (id_kajian, id_pemateri) values (%s, %s)", [id_kajian, id_pemateri])
            # cur.execute("insert into kajian_poster (id_kajian, poster_path) values (%s, %s)", [id_kajian, poster_path])

            # if (id_kajian !== None):
            #     conn.commit()
            #     result = {responseCode:"200", responseText:"success", _id:str(id_kajian)}
            # else:
            result = {responseCode:"401", responseText:"Please try again"}    
        else:
            result = {responseCode:"401", responseText:"Ooppss..."}

    except Exception as e:
        result = {responseCode:"404", responseText:"Not found", detail:str(e)}
    finally:
        CloseDB(conn, cur)
    return result