from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB

app = Flask(__name__)

responseCode="response_code"
responseText="response_text"
responseList="response_list"
sessionToken="session_token"
detail="detail"

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