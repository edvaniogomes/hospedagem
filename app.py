from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()  
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT NOT NULL UNIQUE)''') 
    conn.commit()  
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

@app.route("/adicionar", methods=["POST"])
def adicionar_usuario():
    nome = request.form["nome"]
    email = request.form["email"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()  
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))  
    conn.commit()  
    conn.close()

    return redirect('/')

# Executando o aplicativo
if __name__ == "__main__":
    init_db()  
    app.run(debug=True)
