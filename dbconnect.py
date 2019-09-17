from flask import Flask
import psycopg2
import os

DATABASE_URL = os.environ['postgres://qugjbrgnwcorxs:51ba6fbd895d056e4446b56d23a539673b496ffe78ca3fe95ea00315d1e7e32b@ec2-54-221-215-228.compute-1.amazonaws.com:5432/db1ee1t553hrtj']

def ConnectDB():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        return conn, cur
    except:
        print("Error executing select")

def CloseDB(conn, cur):
    conn.close()
    cur.close()
