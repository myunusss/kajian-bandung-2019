from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from flask_bcrypt import Bcrypt
import hashlib

todos = {}

app = Flask(__name__)
bcrypt = Bcrypt(app)

responseCode="response_code"
responseText="response_text"
sessionToken="session_token"
detail="detail"

class SignIn(Resource):
    def post(self):

        if (request.form.get("uname") != None):
            username = request.form.get("uname")
        else:
            username = ""
        
        if (request.form.get("upass") != None):
            password = request.form.get("upass")
        else:
            password = ""
        
        if (request.form.get("di") != None):
            device_id = request.form.get("di")
        else:
            device_id = ""
        
        if (request.form.get("ut") != None):
            user_token = request.form.get("ut")
        else:
            user_token= ""

        salt = "2m-6CN6C4QRe8=2Xep8G"

        try:
            conn, cur = ConnectDB()
            cur.execute("select therapist_id, therapist_name, login_password from therapist where login_id = %s", [username])
            data = cur.fetchone()

            print("DATA", data)
            if (data != None):
                ther_id = data[0]
                ther_name = data[1]
                ther_pass = data[2]

                dataArray = []
                result = []

                if (bcrypt.check_password_hash(ther_pass, password)):

                    if (ther_id > 0):
                        valid_token = hashlib.md5(username+salt+device_id+password.encode())

                        # pengecekan user token
                        if (user_token == valid_token.hexdigest()):
                            # pengecekan pertama pada session untuk id tersebut
                            cur.execute("select count(therapist_id) as session_count from ther_session where therapist_id = %s and device_id = %s and login_time is not null and logout_time is null", [ther_id, device_id])
                            sessionCount = cur.fetchone()[0]

                            # jika sama sekali belum pernah login, maka lakukan insert
                            if (sessionCount == 0):
                                cur.execute("insert into ther_session (therapist_id, device_id, user_token) values (%s,%s,%s)", [ther_id, device_id, user_token])
                                cur.execute("update therapist set therapist_status = %s where therapist_id = %s", [1, ther_id])
                                cur.execute("update attendance set clock_in = current_timestamp where therapist_id = %s", [ther_id])

                                conn.commit()

                                session_token = hashlib.md5(user_token+device_id.encode())

                                result = {responseCode:"200", responseText:"Success", sessionToken:session_token.hexdigest()}
                                
                            # jika sudah pernah sign in, maka cek user token
                            else:
                                cur.execute("select user_token from ther_session where therapist_id = %s and device_id = %s and login_time is not null and logout_time is null", [ther_id, device_id])
                                db_user_token = cur.fetchone()

                                # cek user token pada tabel apakah sama dengan user token dari user
                                if (db_user_token != None and db_user_token[0] == user_token):
                                    # update therapist status
                                    cur.execute("update therapist set therapist_status = %s where therapist_id = %s", [0, ther_id]) #SET DEFAULT KE OFF/REST

                                    session_token = hashlib.md5(user_token+device_id.encode())
                                    result = {responseCode:"200", responseText:"Success", sessionToken:session_token.hexdigest()}
                                
                                # jika berbeda, buat session baru
                                else:
                                    cur.execute("insert into ther_session (therapist_id, device_id, user_token) values (%s,%s,%s)", [ther_id,device_id,user_token])
                                    # update therapist status
                                    cur.execute("update therapist set therapist_status = %s where therapist_id = %s", [0, ther_id]) #SET DEFAULT KE OFF/REST

                                    conn.commit()

                                    session_token = hashlib.md5(user_token+device_id.encode())
                                    result = {responseCode:"200", responseText:"Success", sessionToken:session_token.hexdigest()}

                        else:
                            result = {responseCode:"401", responseText:"Not valid token"}
                    else:
                        result = {responseCode:"401", responseText:"Username undefined"}
                else:
                    result = {responseCode:"401", responseText:"Wrong Password"}
            else:
                result = {responseCode:"401", responseText:"Username undefined"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)
        
        print(result)

        return result