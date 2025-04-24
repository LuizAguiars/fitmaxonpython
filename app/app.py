from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'secreto'

# -------------------- Configuração de Conexão -------------------- #


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='8474',
        database='fitmaxgym'
    )

# -------------------- Rotas do Sistema -------------------- #


@app.route('/')
def home():
    return render_template('inicial.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT Senha_User, Nome_User FROM USUARIO WHERE Email_user = %s", (email,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if resultado is None:
            flash("E-mail não cadastrado!", "error")
            return redirect(url_for('login'))

        senha_correta, nome = resultado
        if senha != senha_correta:
            flash("Senha incorreta!", "error")
            return redirect(url_for('login'))

        session['usuario'] = nome
        return redirect(url_for('inicial_logado'))

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID_PLANO, nome_plano FROM PLANO")
    planos = cur.fetchall()
    cur.close()
    conn.close()

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
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO USUARIO
                (Nome_User, Email_user, Senha_User, cpf_user, Data_Cadastro_user,
                 sexo_user, endereco_user, CEP_USER, ID_PLANO, status_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, email, senha, cpf, data, sexo, endereco, cep, id_plano, 'Ativo'))
            conn.commit()
            cur.close()
            conn.close()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError as e:
            if "Email_user" in str(e):
                flash("E-mail já cadastrado!", "error")
            elif "cpf_user" in str(e):
                flash("CPF já cadastrado!", "error")
            else:
                flash("Erro ao cadastrar. Tente novamente.", "error")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html', planos=planos)


@app.route('/inicial-logado')
def inicial_logado():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))

    nome_completo = session['usuario']
    primeiro_nome = nome_completo.split()[0]

    response = make_response(render_template(
        'iniciallogado.html', nome=primeiro_nome))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Você saiu da sua conta com sucesso!", "success")
    return redirect(url_for('login'))


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


@app.route('/gestao-personal')
def gestao_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão dos personal trainers.", "error")
        return redirect(url_for('login'))
    return render_template('gestao_personal.html')


@app.route('/gestao-usuarios')
def gestao_usuarios():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de usuários.", "error")
        return redirect(url_for('login'))
    return render_template('gestao_usuarios.html')


@app.route('/gestao-equipamentos')
def gestao_equipamentos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de equipamentos.", "error")
        return redirect(url_for('login'))
    return render_template('gestao_equipamentos.html')


@app.route('/gestao-unidades', methods=['GET', 'POST'])
def gerenciar_unidade():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de unidades.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        capacidade = request.form.get('capacidade')
        fone = request.form.get('fone')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        id_regiao = request.form.get('id_regiao')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO UNIDADES 
                    (Nome_Unidade, Endereco_Unidade, Capacidade, Fone, Cidade, Estado, CEP, ID_Regiao)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (nome, endereco, capacidade, fone, cidade, estado, cep, id_regiao))
                flash("Unidade incluída com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE UNIDADES 
                    SET Nome_Unidade=%s, Endereco_Unidade=%s, Capacidade=%s, Fone=%s, Cidade=%s, Estado=%s, CEP=%s, ID_Regiao=%s 
                    WHERE ID_Unidades=%s
                """, (nome, endereco, capacidade, fone, cidade, estado, cep, id_regiao, id))
                flash("Unidade alterada com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM UNIDADES WHERE ID_Unidades=%s", (id,))
                flash("Unidade removida com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # 👇 JOIN para exibir o nome da região
    cursor.execute("""
        SELECT u.*, r.Nome_Regiao 
        FROM UNIDADES u
        JOIN REGIAO r ON u.ID_Regiao = r.ID_Regiao
    """)
    unidades = cursor.fetchall()

    # 👇 Para o dropdown
    cursor.execute("SELECT * FROM REGIAO")
    regioes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('gestao_unidades.html', unidades=unidades, regioes=regioes)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
