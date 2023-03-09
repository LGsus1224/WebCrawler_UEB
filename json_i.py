from database import requestConnection, requestCursor
import time
import datetime
import json
import os
os.environ.keys()
# Leer el archivo JSON
with open('datos.json', 'r') as f:
    datos = json.load(f)


db = requestConnection()
cursor = requestCursor(db)
# Crear una tabla si no existe

cursor.execute(
    "CREATE TABLE IF NOT EXISTS websites (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), tittle VARCHAR(255), dominio VARCHAR(255), route VARCHAR(255), extension VARCHAR(20),fecha varchar(10),hora varchar(8))")
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_time = time.strftime("%H:%M:%S")
# Insertar los valores en la tabla
for da in datos:
    ruta = da["RUTA"]
    url = da["URL"]
    dominio = da["DOMINIO"]
    if ruta.startswith("/"):
        ruta = ruta.lstrip("/")

    sql = "INSERT INTO websites (url, tittle,dominio, route,extension,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (url, "title", dominio, ruta, "", current_date, current_time)

    cursor.execute(sql, val)

# Confirmar los cambios y cerrar la conexión
db.commit()
cursor.close()
db.close()
