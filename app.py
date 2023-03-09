from flask import Flask, render_template,url_for,redirect,request,flash
from flask_wtf import CSRFProtect
from database import requestConnection,requestCursor
import re
import requests
from bs4 import BeautifulSoup
import datetime
import time
app = Flask(__name__)

crsf = CSRFProtect(app)

app.secret_key = '9a08a27ae4a8210bd2bc3fbc96282c7adfc5c82b0a03c4e3067cec99bb8e9eb6'
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_time = time.strftime("%H:%M:%S")
def insertST(cursor,lista,title,filtro):
    for i in lista:
        ru = ""
        try:
            ru = i.split("/", 3)[3]
        except:
            ru = ""
        sql = ("INSERT INTO weblinks(url,title,domain,route,filt,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        
        
        
        val = (i, title, str(i.split("/")[2]), ru, filtro,current_date,current_time)
        cursor.execute(sql,val)
        
        
        
        
        cursor.connection.commit()

def deleteST(cursor,lista,nueva,title,filtro):
    for i in lista:
        cursor.execute("DELETE FROM weblinks WHERE id=%s",(i['id']))
        cursor.connection.commit()
    insertST(cursor,nueva,title,filtro)

def updateST(cursor,original,lista,title,filtro):
    for i in range(len(lista)):
        if len(lista)==len(original):
            ru = ""
            try:
                ru = lista[i].split("/", 3)[3]
            except:
                ru = ""
            sql = "UPDATE weblinks SET url='%s',title='%s',domain='%s',route='%s',fecha='%s' ,hora='%s'  WHERE id=%s"
            val = (lista[i], title, str(lista[i].split("/")[2]), ru, original[i]['id'],current_date,current_time)
            cursor.execute(sql,val)
            cursor.connection.commit()
        elif len(lista)>len(original):
            ru = ""
            try:
                ru = lista[i].split("/", 3)[3]
            except:
                ru = ""
            if i<len(original):
                sql = "UPDATE weblinks SET url='%s',title='%s',domain='%s',route='%s' WHERE id=%s"
                val = (lista[i], title, str(lista[i].split("/")[2]), ru, original[i]['id'])
            else:
                sql = ("INSERT INTO weblinks(url,title,domain,route,filt,fecha,hora) VALUES (%s, %s, %s, %s, %s, %s, %s)")
                val = (lista[i], title, str(lista[i].split("/")[2]), ru, filtro,current_date,current_time)
            cursor.execute(sql,val)
            cursor.connection.commit()
        elif len(lista)<len(original):
            ru = ""
            try:
                ru = lista[i].split("/", 3)[3]
            except:
                ru = ""
            if i<len(lista):
                sql = "UPDATE weblinks SET url='%s',title='%s',domain='%s',route='%s',fecha='%s' ,hora='%s'  WHERE id=%s"
                val = (lista[i], title, str(lista[i].split("/")[2]), ru, original[i]['id'],current_date,current_time)
            else:
                cursor.execute("DELETE FROM weblinks WHERE id=%s",(lista[i]['id']))
                cursor.connection.commit()

def consulta(cursor,filtro, texto):
    filters = {'web':'a','images':'img'}
    get_source = {'web':'href','images':'src'}
    # Hacer scraping de datos de un sitio web
    url = "https://www.ueb.edu.ec"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Extraer los datos relevantes
    title = soup.title.string
    # Buscar los elementos por filtro
    links = soup.find_all(filters[filtro])
    all_links = []
    for link in links:
        # Obtener la ruta correspodiente a cada elemento según filtro
        href = link.get(get_source[filtro])
        if href.startswith('http'):
            all_links.append(str(href))
        else:
            all_links.append(str(url+href))
    all_links = set(all_links)
    cursor.execute(
            "CREATE TABLE IF NOT EXISTS weblinks (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255), title VARCHAR(255), domain VARCHAR(255), route VARCHAR(200),filt ENUM('web','images','videos','pdf'),fecha varchar(200),hora varchar(200))")

    #  Tomar los links exitentes y no existentes de la DB a partir de todos los links del webcrawler
    cursor.execute("SELECT id,url FROM weblinks WHERE url NOT IN %s AND filt = %s ",(all_links,filtro))
    no_exist_links = cursor.fetchall()
    cursor.execute("SELECT id,url FROM weblinks WHERE url IN %s AND filt = %s",(all_links,filtro))
    exist_links = cursor.fetchall()
    # Si está vacía la estructura insertar todos los links
    if len(exist_links)==0 and len(no_exist_links)==0:
        insertST(cursor,all_links,title,filtro)
    elif len(exist_links)>0 and len(no_exist_links)>0:
        for i in exist_links:
            all_links.remove(i['url'])
        deleteST(cursor,no_exist_links,all_links,title,filtro)
    elif len(exist_links)>0 and len(no_exist_links)==0:
        for i in exist_links:
            all_links.remove(i['url'])
        insertST(cursor,all_links,title,filtro)
    elif len(exist_links)==0 and len(no_exist_links)>0 and len(no_exist_links)==len(all_links):
        updateST(cursor,no_exist_links,all_links,title,filtro)
    elif len(exist_links)==0 and len(no_exist_links)>0 and len(no_exist_links)<len(all_links):
        updateST(cursor,no_exist_links,all_links,title,filtro)



@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('home',filtro='web'))

@app.route('/<string:filtro>', methods=['GET','POST'])
def home(filtro):
    if request.method=='GET':
        filters = {'web':'Web','images':'Images'}
        if filtro in filters:
            return render_template('index.html',filters=filters,c_filter=filtro)
        else:
            return redirect(url_for('home',filtro='web'))
    else:
        texto = request.form['search_text']
        if len(texto) == 0 or re.search(r'\W', texto):
            flash('Texto ingresado no válido', 'error')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('search_text',filtro=filtro,texto=str(texto)))

@app.route('/search/<string:filtro>/<string:texto>',methods=['GET','POST'])
def search_text(filtro,texto):
    db=requestConnection()
    cursor=requestCursor(db)
    if request.method == 'GET':
        filters = {'web':'Web','images':'Images'}
        if filtro in filters:
            consulta(cursor,filtro,texto)
            cursor.execute(f"SELECT * FROM weblinks WHERE url LIKE '%{texto}%' AND filt='{filtro}'")
            datos=cursor.fetchall()
            cursor.close()
            db.close()
            return render_template('load_content.html',filtror=filtro, texto=texto, datos=datos, filters=filters, c_filter=filtro)
        else:
            cursor.close()
            db.close()
            return redirect(url_for('search_text',filtro='web',texto=texto))
    else:
        texto = request.form['search_text']
        if len(texto) == 0 or re.search(r'\W', texto):
            flash('Texto ingresado no válido', 'error')
            cursor.close()
            db.close()
            return redirect(url_for('index'))
        else:
            cursor.close()
            db.close()
            return redirect(url_for('search_text',filtro=filtro,texto=str(texto)))

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)