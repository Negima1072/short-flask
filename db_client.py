import pymysql.cursors
import os

def mysql():
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        user="short",
        password=os.environ["MYSQL_PASSWORD"],
        charset="utf8"
    )
