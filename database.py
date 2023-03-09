import pymysql.cursors

h = 'localhost'
d = 'crawler_db'
u = 'root'
p = ''

def requestConnection():
    db_conn = pymysql.connect(host=h, user=u, password=p, database=d)
    return db_conn


def requestCursor(conn):
    return pymysql.cursors.DictCursor(conn)
