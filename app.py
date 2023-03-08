from flask import Flask, render_template,url_for,redirect,request,flash
from flask_wtf import CSRFProtect
from database import requestConnection,requestCursor
import re

app = Flask(__name__)

crsf = CSRFProtect(app)

app.secret_key = '9a08a27ae4a8210bd2bc3fbc96282c7adfc5c82b0a03c4e3067cec99bb8e9eb6'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:
        texto = request.form['search_text']
        if len(texto) == 0 or re.search(r'\W', texto):
            flash('Texto ingresado no válido', 'error')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('search_text',texto=str(texto)))

@app.route('/search/<string:texto>',methods=['GET','POST'])
def search_text(texto):
    if request.method == 'GET':
        db=requestConnection()
        cursor=requestCursor(db)
        cursor.execute(f"SELECT * FROM websites WHERE url LIKE '%{texto}%'")
        datos=cursor.fetchall()
        return render_template('load_content.html', texto=texto, datos=datos)
    else:
        texto = request.form['search_text']
        if len(texto) == 0 or re.search(r'\W', texto):
            flash('Texto ingresado no válido', 'error')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('search_text',texto=str(texto)))

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)