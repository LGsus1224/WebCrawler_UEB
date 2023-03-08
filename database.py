import mysql.connector


def connect_to_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crawler_db"
    )
    return db
