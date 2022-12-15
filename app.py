from flask import Flask, redirect, request
from db_client import mysql
from urlparse import urlparse
import random, string

def randomstr(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

app = Flask(__name__)

def db_initialize():
    with mysql() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS short")
            conn.commit()
        with conn.cursor() as cur:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS short.ijij_cf (
                    id int(10) NOT NULL NOT_INCREMENT PRIMARY KEY,
                    page_id varchar(6) NOT NULL,
                    url varchar(255) NOT NULL
                )
                '''
            )
            conn.commit()

@app.route("/")
def index():
    return "TopPage"

@app.route("/<page_id>")
def page(page_id):
    with mysql() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM short.ijij_cf WHERE page_id  = %s", (page_id))
            result = cur.fetchall()
            if len(result) == 0:
                return "NotFound", 404
            else:
                return redirect(result[0][2])
    return "ServerError", 500

@app.route("/api/short")
def short():
    url = request.args.get("url", "")
    o = urlparse(url)
    if len(o.scheme) <= 0:
        return "BadRequest", 400
    with mysql() as conn:
        with conn.cursor() as cur:
            trycount = 0
            while True:
                trycount += 1
                page_id = randomstr(5)
                cur.execute("SELECT id from short.ijij_cf WHERE page_id = %s", (page_id))
                result = cur.fetchall()
                if len(result) <= 0:
                    with conn.cursor() as cur2:
                        cur2.execute("INSERT INTO short.ijij_cf(page_id, url) VALUES(%s, %s)", (page_id, url))
                        conn.commit()
                    return "https://ijij.cf/"+page_id
                if trycount >= 5:
                    return "TooManyData", 500
    return "ServerError", 500

if __name__ == '__main__':
    db_initialize()
    app.run(port=80)
