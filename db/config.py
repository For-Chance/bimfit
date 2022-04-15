import pymysql


def configDB():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="bimfit",
        autocommit=1,
    )
    return db.cursor()
