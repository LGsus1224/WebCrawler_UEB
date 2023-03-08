import mysql.connector
import requests
from bs4 import BeautifulSoup
from datetime import datetime
now = datetime.now()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crawler_db"
)
cursor = db.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS websites (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), title VARCHAR(255), description TEXT,fecha varchar(10),hora varchar(8))")


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
        sql = "INSERT INTO websites (url) VALUES (%s)"
        val = (href,)
        cursor.execute(sql, val)
        db.commit()
