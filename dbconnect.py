from flask import Flask
import psycopg2

def ConnectDB():
    connectionString = 'dbname=db1ee1t553hrtj host=ec2-54-221-215-228.compute-1.amazonaws.com user=qugjbrgnwcorxs password=51ba6fbd895d056e4446b56d23a539673b496ffe78ca3fe95ea00315d1e7e32b port=5432'
    
    try:
        conn = psycopg2.connect(connectionString, sslmode='require')
        cur = conn.cursor()

        conn.autocommit=False
        
        return conn, cur
    except:
        print("Error executing select")

def CloseDB(conn, cur):
    
    conn.close()
    cur.close()
