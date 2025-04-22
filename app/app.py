from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
from flask import make_response

app = Flask(__name__)
app.secret_key = 'secreto'

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '8474'
app.config['MYSQL_DB'] = 'fitmaxgym'

mysql = MySQL(app)

# Rota inicial


@app.route('/')
def home():
    return render_template('inicial.html')

# Rota de login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT Senha_User, Nome_User FROM USUARIO WHERE Email_user = %s", (email,))
        resultado = cur.fetchone()
        cur.close()

        if resultado is None:
            flash("E-mail não cadastrado!", "error")
            return redirect(url_for('login'))

        senha_correta, nome = resultado
        if senha != senha_correta:
            flash("Senha incorreta!", "error")
            return redirect(url_for('login'))

        session['usuario'] = nome  # ← ESSENCIAL estar aqui antes do redirect
        return redirect(url_for('inicial_logado'))

    return render_template('login.html')


# Rota de cadastro


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
   # flash("⚠️ Testando exibição de flash!", "error")

    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_PLANO, nome_plano FROM PLANO")
    planos = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        data = request.form['data']
        sexo = request.form['sexo']
        endereco = request.form['endereco']
        cep = request.form['cep']
        id_plano = request.form['plano']

        if len(cpf) > 14:
            flash("CPF inválido. Deve ter no máximo 14 caracteres.", "error")
            return redirect(url_for('cadastro'))

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO USUARIO 
                (Nome_User, Email_user, Senha_User, cpf_user, Data_Cadastro_user, sexo_user, endereco_user, CEP_USER, ID_PLANO, status_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, email, senha, cpf, data, sexo, endereco, cep, id_plano, 'Ativo'))
            mysql.connection.commit()
            cur.close()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('login'))

        except IntegrityError as e:
            if "Email_user" in str(e):
                flash("E-mail já cadastrado!", "error")
            elif "cpf_user" in str(e):
                flash("CPF já cadastrado!", "error")
            else:
                flash("Erro ao cadastrar. Tente novamente.", "error")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html', planos=planos)

# após login


@app.route('/inicial-logado')
def inicial_logado():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))

    nome_completo = session['usuario']
    primeiro_nome = nome_completo.split()[0]

    # 🔒 Protege contra cache
    response = make_response(render_template(
        'iniciallogado.html', nome=primeiro_nome))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# deslogar

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Você saiu da sua conta com sucesso!", "success")
    return redirect(url_for('login'))

# Paineis de Gestão


@app.route('/painel-gestor')
def painel_gestor():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do gestor.", "error")
        return redirect(url_for('login'))
    return render_template('paineldogestor.html')


@app.route('/painel-personal')
def painel_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do personal.", "error")
        return redirect(url_for('login'))
    return render_template('paineldopersonal.html')


@app.route('/minha-conta')
def minha_conta():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar sua conta.", "error")
        return redirect(url_for('login'))
    return render_template('minhaconta.html')


# Rodando a aplicação
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
