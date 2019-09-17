from flask import Flask
import psycopg2

def ConnectDB():
    dbname = "_spa"
    host = "192.168.1.100"
    user = "postgres"
    pwd = "admin"
    port = "5432"

    connectionString = 'dbname=_spa host=192.168.1.100 user=postgres password=admin port=5432'
    
    try:
        conn = psycopg2.connect(connectionString)
        cur = conn.cursor()

        conn.autocommit=False
        
        return conn, cur
    except:
        print("Error executing select")

def CloseDB(conn, cur):
    
    conn.close()
    cur.close()
