from flask import Flask, request
from flask_restful import Resource, Api
from dbconnect import ConnectDB, CloseDB
from flask_bcrypt import Bcrypt
import hashlib
from common.app_setting import responseCode, responseText, detail, sessionToken, appID, myID

todos = {}

app = Flask(__name__)
bcrypt = Bcrypt(app)

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

        if (request.form.get("fcmtkn") != None):
            fcm_token = request.form.get("fcmtkn")
        else:
            fcm_token= ""

        salt = "2m-6CN6C4QRe8=2Xep8G"

        conn, cur = ConnectDB()
        try:
            cur.execute("select therapist_id, therapist_name, login_password, therapist_status from therapist where lower(login_id) = lower(trim(%s)) and coalesce(suspended, 0) = 0", [username])
            data = cur.fetchone()

            if (data != None):
                ther_id = data[0]
                ther_name = data[1]
                ther_pass = data[2]
                ther_stat = data[3]

                # cek status terakhir, jika working jangan diganti
                if (ther_stat == 3):
                    ther_stat = ther_stat
                else :
                    ther_stat = 1

                dataArray = []
                result = []
                temp_str = str(username) + str(salt) + str(device_id) + str(password)

                if (bcrypt.check_password_hash(ther_pass, password)):
                    if (ther_id > 0):
                        valid_token = hashlib.md5(temp_str.encode('utf-8'))

                        # update fcm token
                        cur.execute("update therapist set fcm_client_token = %s " +
                        "where therapist_id = %s", [fcm_token, ther_id])

                        # pengecekan user token dari hp dengan api (bukan db)
                        if (user_token == valid_token.hexdigest()):
                            # pengecekan pertama pada session dan attendance berdasarkan user token(device_id)
                            cur.execute("select count(therapist_id) as session_count, " +
                            "(select count(therapist_id) from attendance where therapist_id = %s and date(clock_in) = current_date and clock_out is null) " +
                            "from ther_session where therapist_id = %s and device_id = %s and login_time is not null and logout_time is null", [ther_id, ther_id, device_id])
                            d_count = cur.fetchone()
                            sessionCount = d_count[0]
                            attendanceCount = d_count[1]

                            # jika sama sekali belum pernah sign in, maka lakukan insert ther_session dan attendance
                            if (sessionCount == 0 and attendanceCount == 0):
                                cur.execute("insert into ther_session (therapist_id, device_id, user_token) values (%s,%s,%s)", [ther_id, device_id, user_token])
                                cur.execute("update therapist set therapist_status = %s where therapist_id = %s", [ther_stat, ther_id])
                                cur.execute("insert into attendance (therapist_id, clock_in) values (%s,current_timestamp)", [ther_id])

                                session_token = hashlib.md5(temp_str.encode('utf-8'))

                                result = {
                                    responseCode:"200",
                                    responseText:"Success",
                                    sessionToken:session_token.hexdigest(),
                                    appID:myID
                                }
                            
                            # jika sudah pernah sign in dengan device berbeda
                            elif (sessionCount == 0 and attendanceCount != 0):
                                cur.execute("insert into ther_session (therapist_id, device_id, user_token) values (%s,%s,%s)", [ther_id, device_id, user_token])
                                cur.execute("update therapist set therapist_status = %s where therapist_id = %s", [ther_stat, ther_id])

                                session_token = hashlib.md5(temp_str.encode('utf-8'))

                                result = {
                                    responseCode:"200",
                                    responseText:"Success",
                                    sessionToken:session_token.hexdigest(),
                                    appID:myID
                                }

                            # jika sudah pernah sign in dengan device yang sama dan logout null 
                            else:
                                session_token = hashlib.md5(temp_str.encode('utf-8'))
                                result = {
                                    responseCode:"200",
                                    responseText:"Success",
                                    sessionToken:session_token.hexdigest(),
                                    appID:myID
                                }
                        
                        else:
                            result = {responseCode:"401", responseText:"Not valid token"}
                    else:
                        result = {responseCode:"401", responseText:"Username undefined"}
                else:
                    result = {responseCode:"401", responseText:"Wrong Password"}
            else:
                result = {responseCode:"401", responseText:"Username undefined"}
            
            conn.commit()

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result

class UpdateAttendance(Resource):
    def post(self):
        if (request.form.get("uname") != None):
            username = request.form.get("uname")
        else:
            username = ""

        if (request.form.get("stkn") != None):
            session_token = request.form.get("stkn")
        else:
            session_token = ""
        
        if (request.form.get("di") != None):
            device_id = request.form.get("di")
        else:
            device_id = ""

        if (request.form.get("ther_id") != None):
            therapist_id = request.form.get("ther_id")
        else:
            therapist_id = ""

        conn, cur = ConnectDB()
        try:
            if (therapist_id != ""):
                cur.execute("insert into attendance (therapist_id, clock_in) values (%s,current_timestamp)", [therapist_id])
                conn.commit()
            
                result = {responseCode:"200", responseText:"Absen berhasil"}
            else :
                result = {responseCode:"401", responseText:"Therapist tidak ditemukan"}

        except Exception as e:
            result = {responseCode:"404", responseText:"failed", detail:str(e)}
            conn.rollback()

        finally:
            CloseDB(conn, cur)

        return result