from flask import Flask, redirect, request
from db_client import 
from urlparse import urlparse

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
            cur.execute("")


if __name__ == '__main__':
    db_initialize()
    app.run(port=80)