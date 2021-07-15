import datetime
import random

from flask import Flask, render_template, request
import sqlite3 as sq

from werkzeug.utils import redirect

banco = sq.connect('banco.db', check_same_thread=False)
cursor = banco.cursor()

if sq.connect('banco.db'):
    print('* Cliente de dados conectado com sucesso!')
else:
    print('Um erro ocorreu ao tentar-se conectar em "banco.db"!')

cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (user text, password text, id text, time text)")
cursor.execute("CREATE TABLE IF NOT EXISTS posts (conteudo text, id text, autor text, likes integer)")


app = Flask(__name__) # Instanciando classe

def msg(msg):
    print(msg)

@app.route('/') # Criando rota principal
def index():
    return render_template('index.html', titulo='Página inicial')

@app.route('/sobre')
def inicio():
    return '<h1> Sobre <h1>'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/homepage_cadastro', methods=['POST'])
def homepage_cadastro():
    name = request.form['nome']
    senha = request.form['password']
    id = random.randint(10000000000000, 1000000000000000)
    x = datetime.datetime.now()
    cursor.execute("INSERT INTO usuarios VALUES ('" + str(name) + "', '" + str(
        senha) + "', '" + str(id) + "', '" + str(x) + "')")
    banco.commit()
    return render_template('homepage.html')

@app.route('/homepage_login', methods=['POST'])
def homepage_login():
    name = request.form['nome']
    senha = request.form['password']
    cursor.execute("SELECT password FROM usuarios WHERE user='"+str(name)+"'")
    mesg = f'{cursor.fetchall()}'
    if mesg == '[]':
        return render_template('index_senha_incorreta.html')
    else:
        return render_template('homepage.html')

@app.route('/homepage_cadastro_post', methods=['POST'])
def homepage_cadastro_post():
    post = request.form['post']
    usuario = homepage_cadastro.__name__
    id = random.randint(10000000000000, 1000000000000000)
    cursor.execute("INSERT INTO posts VALUES ('"+str(post)+"', '"+str(id)+"', '"+str(usuario)+"' , 0)")
    banco.commit()
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
    
