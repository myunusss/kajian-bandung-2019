from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from common.app_setting import responseCode, responseText, detail, sessionToken

app = Flask(__name__)

class AppAuth(Resource):
    def post(self):

        if (request.form.get("app_id") != None):
            app_id = request.form.get("app_id")
        else:
            app_id = ""

        try:

            url = 'http://192.168.1.214:5001/'

            result = {
                responseCode:"200", responseText:"Success", "prefix":str(url)
            }

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}

        return result

class ButtonAndStatus(Resource):
    def post(self):
        if (request.form.get("stkn") != None):
            sessionToken = request.form.get("stkn")
        else:
            sessionToken = ""

        try:
            Button = ["Terima", "Saya sudah di Room", "Tamu sudah di Room", "Memulai Sesi", "Mengakhiri Sesi", "Saya Meninggalkan Room"];
            Status = ["Segera Terima Order", "Persiapan Menuju Ruangan", "Menunggu Tamu", "Siap Memulai Sesi", "Sesi Sudah Dimulai", "Selesai"];

            result = {
                responseCode:"200", responseText:"Success", "button":Button, "status":Status
            }

        except Exception as e:
            result = {responseCode:"404", responseText:"Failed", detail:str(e)}

        return result