from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from db import get_db_connection
from validacoes import validar_cpf, validar_nome

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT ID_User, Senha_User, Nome_User FROM USUARIO WHERE Email_user = %s", (email,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if resultado is None:
            flash("E-mail não cadastrado!", "error")
            return redirect(url_for('auth.login'))

        id_user, senha_correta, nome = resultado
        if senha != senha_correta:
            flash("Senha incorreta!", "error")
            return redirect(url_for('auth.login'))

        session['usuario'] = id_user
        session['nome'] = nome

        return redirect(url_for('home.inicial_logado'))

    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Você saiu da sua conta com sucesso!", "success")
    return redirect(url_for('auth.login'))

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
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
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        sexo = request.form['sexo']
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        id_plano = request.form['plano']

        if len(cpf) > 14:
            flash("CPF inválido. Deve ter no máximo 14 caracteres.", "error")
            return redirect(url_for('auth.cadastro'))

        if not validar_cpf(cpf):
            flash("CPF inválido. Digite um CPF real e válido.", "error")
            return redirect(url_for('auth.cadastro'))

        import re
        telefone_numerico = re.sub(r'\D', '', telefone)
        if not telefone_numerico.isdigit() or len(telefone_numerico) not in [10, 11]:
            flash("Telefone inválido. Use um número válido com DDD.", "error")
            return redirect(url_for('auth.cadastro'))

        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)

            cur.execute("SELECT * FROM USUARIO WHERE cpf_user = %s", (cpf,))
            if cur.fetchone():
                flash("CPF já cadastrado!", "error")
                cur.close()
                conn.close()
                return redirect(url_for('auth.cadastro'))

            cur.execute(
                "SELECT * FROM USUARIO WHERE Email_user = %s", (email,))
            if cur.fetchone():
                flash("E-mail já cadastrado!", "error")
                cur.close()
                conn.close()
                return redirect(url_for('auth.cadastro'))

            if not validar_nome(nome):
                flash("Nome inválido. O nome deve conter apenas letras.", "error")
                return redirect(url_for('auth.cadastro'))

            cur.execute("""
                INSERT INTO USUARIO
                (Nome_User, Email_user, Senha_User, cpf_user, Data_Nascimento,
                 sexo_user, CEP_USER, logradouro_user, numero_user,
                 bairro_user, cidade_user, estado_user, telefone_user, ID_PLANO, status_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nome, email, senha, cpf, data_nascimento, sexo, cep,
                logradouro, numero, bairro, cidade, estado, telefone,
                id_plano, 'Ativo'
            ))

            conn.commit()
            cur.close()
            conn.close()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f"Erro ao cadastrar: {str(e)}", "error")
            return redirect(url_for('auth.cadastro'))

    return render_template('cadastro.html', planos=planos) 