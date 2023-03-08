import pymysql.cursors

h = ''
d = ''
u = ''
p = ''
port = ''
db = pymysql.connect(host=h,user=u,password=p,database=d,port=port)
cursor = pymysql.cursors.DictCursor(db)