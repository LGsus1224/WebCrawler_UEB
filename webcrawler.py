import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import requestConnection, requestCursor

now = datetime.now()

db=requestConnection()
cursor = requestCursor(db)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS websites (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), tittle VARCHAR(255), dominio VARCHAR(255), route VARCHAR(255),fecha varchar(10),hora varchar(8))")


# Hacer scraping de datos de un sitio web
url = "https://www.ueb.edu.ec/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extraer los datos relevantes
title = soup.title.string
description = soup.find("meta", {"name": "description"})
if description:
    content = description["content"]
else:
    content = ""
# Insertar los datos en la base de datos MySQL
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href.startswith('http'):
        # Insertar los enlaces en la base de datos MySQL
        sql = "INSERT INTO websites (url, tittle,dominio, route,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s)"
        ru = ""
        try:
            ru = href.split("/", 3)[3]
        except:
            ru = ""
        val = (href, title, str(href.split("/")[2]), ru, ((str(now.day)+"/" + str(now.month)+"/" + str(now.year))),
                (str(now.hour) + ":"+str(now.minute)+":"+str(now.second)))
        cursor.execute(sql, val)
        cursor.connection.commit()
cursor.close()
db.close()