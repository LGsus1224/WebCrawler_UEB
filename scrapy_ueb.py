

import scrapy

import requests


url = "https://www.ueb.edu.ec/"

class UebSpider(scrapy.Spider):

    name = 'ueb'

    allowed_domains = ['ueb.edu.ec']

    start_urls = [url]



    def parse(self, response):

        # Extrayendo el título de la página

        title = response.xpath('//title/text()').get()

        # print('Título:', title)


        # Extrayendo los enlaces de la página

        links = response.xpath('//a/@href').getall()

        print('Enlaces:')
        dominio = url
        ruta = ""
        url1=url
        for link in links:
            url1=link

            if link.startswith("http"):

                try:
                    dominio = link.split("/")[2]

                except:
                    dominio = link
                

                try:

                    ruta = link.split("/",3)[3]

                except:

                    ruta = link
                

            else:

                try:
                    dominio = link.split("/")[2]
                    ruta = link.split("/",3)[2]

                except:

                    ruta = link

            yield {"URL":url1, "DOMINIO": dominio, "RUTA": ruta}


