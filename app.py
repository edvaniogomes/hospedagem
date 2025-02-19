from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_secreta"

def get_db_connection():
    """Função para abrir conexão com o banco de dados"""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Retorna os resultados como dicionários
    return conn

def init_db():
    """Inicializa o banco de dados"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nome TEXT NOT NULL,
                          email TEXT NOT NULL UNIQUE)''')
        conn.commit()

@app.route('/')
def index():
    """Carrega a página inicial com a lista de usuários"""
    with get_db_connection() as conn:
        usuarios = conn.execute("SELECT * FROM usuarios").fetchall()  # Obtém os usuários cadastrados
    
    return render_template('index.html', usuarios=usuarios)

@app.route("/adicionar", methods=["POST"])
def adicionar_usuario():
    """Adiciona um novo usuário e recarrega a página"""
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()

    if not nome or not email:
        flash("Nome e e-mail são obrigatórios!", "error")
        return redirect("/")

    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
        flash("Usuário cadastrado com sucesso!", "success")
    except sqlite3.IntegrityError:
        flash("Erro: Este e-mail já está cadastrado!", "error")

    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
