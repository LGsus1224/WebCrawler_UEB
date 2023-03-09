
import scrapy
import requests
from bs4 import BeautifulSoup
import datetime
import time
from database import requestConnection, requestCursor
from ping3 import ping, verbose_ping

now = datetime.now()
db = requestConnection()
cursor = requestCursor(db)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS websites (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), tittle VARCHAR(255), dominio VARCHAR(255), route VARCHAR(255), extension VARCHAR(20),fecha varchar(10),hora varchar(8))")


# Hacer scraping de datos de un sitio web
url = "https://www.ueb.edu.ec/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

# Extraer los datos relevantes
title = soup.title.string
description = soup.find("meta", {"name": "description"})
if description:
    content = description["content"]
else:
    content = ""
# Insertar los datos en la base de datos MySQL

class UebSpider(scrapy.Spider):
    name = 'ueb'
    allowed_domains = ['']
    start_urls = [url]

    def parse(self, response):
        # Extrayendo el título de la página
        title = response.xpath('//title/text()').get()
        #print('Título:', title)

        # Extrayendo los enlaces de la página
        links = response.xpath('//a/@href').getall()
        print('Enlaces:')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = time.strftime("%H:%M:%S")
        for link in links:
            sql = "INSERT INTO websites (url, tittle,dominio, route,extension,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            ru = ""
            try:
                ru = link.split("/", 3)[3]
            except:
                ru = ""

            ex = link.split(".",)[1]
        val = (link, title, str(href.split("/")[2]), ru, ex, current_date, current_time)
        cursor.execute(sql, val)
        cursor.connection.commit()


cursor.close()
db.close()


