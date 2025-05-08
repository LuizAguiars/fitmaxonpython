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
        password='Mateus123',
        database='fitmaxgym'
    )

# -------------------- Rotas do Sistema -------------------- #


@app.route('/')
def home():
    return render_template('inicial.html')

# -------------------- Rotas de tela de login -------------------- #


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

# -------------------- Rotas de tela de cadastro -------------------- #


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

# -------------------- Rotas de tela inicial logado  -------------------- #


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

# -------------------- Rotas de tela de deslogin -------------------- #


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Você saiu da sua conta com sucesso!", "success")
    return redirect(url_for('login'))

# -------------------- Rotas de tela de painel do gestor -------------------- #


@app.route('/painel-gestor')
def painel_gestor():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do gestor.", "error")
        return redirect(url_for('login'))
    return render_template('paineldogestor.html')

# -------------------- Rotas de tela de painel de personal -------------------- #


@app.route('/painel-personal')
def painel_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do personal.", "error")
        return redirect(url_for('login'))
    return render_template('paineldopersonal.html')

# -------------------- Rotas de tela de minha conta -------------------- #


@app.route('/minha-conta')
def minha_conta():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar sua conta.", "error")
        return redirect(url_for('login'))
    return render_template('minhaconta.html')

# -------------------- Rotas de tela de gestão dos personais  -------------------- #


@app.route('/gestao-personal', methods=['GET', 'POST'])
def gestao_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de personais.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        especialidade = request.form.get('especialidade')
        id_unidade = request.form.get('id_unidade')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO PERSONAL (Nome_Personal, Email_Personal, Especialidade, ID_Unidade)
                    VALUES (%s, %s, %s, %s)
                """, (nome, email, especialidade, id_unidade))
                flash("Personal incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE PERSONAL
                    SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s
                    WHERE ID_Personal=%s
                """, (nome, email, especialidade, id_unidade, id))
                flash("Personal alterado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM PERSONAL WHERE ID_Personal=%s", (id,))
                flash("Personal removido com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # JOIN com UNIDADES para exibir nome da unidade
    cursor.execute("""
        SELECT p.*, u.Nome_Unidade
        FROM PERSONAL p
        LEFT JOIN UNIDADES u ON p.ID_Unidade = u.ID_Unidades
    """)
    personais = cursor.fetchall()

    # Lista de unidades para o dropdown
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("gestao_personal.html", personais=personais, unidades=unidades)

# -------------------- Rotas de tela de gestão dos usuarios  -------------------- #


@app.route('/gestao-usuarios', methods=['GET', 'POST'])
def gestao_usuarios():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de usuários.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')  # só usado ao incluir
        cpf = request.form.get('cpf')
        endereco = request.form.get('endereco')
        cep = request.form.get('cep')
        sexo = request.form.get('sexo')
        status = request.form.get('status_cliente')
        pagou = int(request.form.get('pagou_mes_atual') or 0)
        unidade_id = request.form.get('id_unidade')
        plano_id = request.form.get('id_plano')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO USUARIO
                    (Nome_User, Email_user, Senha_User, Data_Cadastro_user, Unidade_Prox_ID,
                     cpf_user, endereco_user, CEP_USER, ID_PLANO, sexo_user, status_cliente, pagou_mes_atual)
                    VALUES (%s, %s, %s, CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, email, senha, unidade_id, cpf, endereco, cep, plano_id, sexo, status, pagou))
                flash("Usuário incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE USUARIO SET
                        Nome_User=%s,
                        Email_user=%s,
                        endereco_user=%s,
                        CEP_USER=%s,
                        sexo_user=%s,
                        status_cliente=%s,
                        pagou_mes_atual=%s,
                        Unidade_Prox_ID=%s,
                        ID_PLANO=%s
                    WHERE ID_User=%s
                """, (nome, email, endereco, cep, sexo, status, pagou, unidade_id, plano_id, id))
                flash("Usuário atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute("DELETE FROM USUARIO WHERE ID_User = %s", (id,))
                flash("Usuário removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # Listar usuários com join
    cursor.execute("""
        SELECT u.*, un.Nome_Unidade, p.nome_plano
        FROM USUARIO u
        LEFT JOIN UNIDADES un ON u.Unidade_Prox_ID = un.ID_Unidades
        LEFT JOIN PLANO p ON u.ID_PLANO = p.ID_PLANO
    """)
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM PLANO")
    planos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('gestao_usuarios.html', usuarios=usuarios, unidades=unidades, planos=planos)

# -------------------- Rotas de tela de gestão dos equipamentos  -------------------- #


@app.route('/gestao-equipamentos', methods=['GET', 'POST'])
def gestao_equipamentos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de equipamentos.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        data_compra = request.form.get('data_compra')
        id_unidade = request.form.get('id_unidade')
        id_status = request.form.get('id_status')
        id_tipo = request.form.get('id_tipo')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO EQUIPAMENTOS
                    (Nome_Equipamento, descricao_equipamentos, data_de_compra,
                     ID_unidade_equipamento, id_status_do_equipamento, idtipo_equipamento)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo))
                flash("Equipamento incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE EQUIPAMENTOS
                    SET Nome_Equipamento=%s, descricao_equipamentos=%s, data_de_compra=%s,
                        ID_unidade_equipamento=%s, id_status_do_equipamento=%s, idtipo_equipamento=%s
                    WHERE ID_equipamentos=%s
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo, id))
                flash("Equipamento atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM EQUIPAMENTOS WHERE ID_equipamentos = %s", (id,))
                flash("Equipamento removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # Consulta completa com JOINs para exibição
    cursor.execute("""
        SELECT e.*, u.Nome_Unidade, s.status_do_Equipamento, t.nome_tipo_equipamento
        FROM EQUIPAMENTOS e
        LEFT JOIN UNIDADES u ON e.ID_unidade_equipamento = u.ID_Unidades
        LEFT JOIN status_dos_Equipamentos s ON e.id_status_do_equipamento = s.idstatus_dos_Equipamentos
        LEFT JOIN tipo_equipamento t ON e.idtipo_equipamento = t.idtipo_equipamento
    """)
    equipamentos = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM status_dos_Equipamentos")
    status_equipamentos = cursor.fetchall()

    cursor.execute("SELECT * FROM tipo_equipamento")
    tipos_equipamento = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'gestao_equipamentos.html',
        equipamentos=equipamentos,
        unidades=unidades,
        status_equipamentos=status_equipamentos,
        tipos_equipamento=tipos_equipamento
    )

# -------------------- Rotas de tela de gestão das unidades  -------------------- #


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

# -------------------- Rotas de tela de gestão dos planos  -------------------- #


@app.route('/gestao-planos', methods=['GET', 'POST'])
def gestao_planos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de planos.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        duracao = request.form.get('duracao')
        valor = request.form.get('valor')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO PLANO (nome_plano, descricao, duracao_meses, valor_plano)
                    VALUES (%s, %s, %s, %s)
                """, (nome, descricao, duracao, valor))
                flash("Plano incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE PLANO
                    SET nome_plano=%s, descricao=%s, duracao_meses=%s, valor_plano=%s
                    WHERE ID_PLANO=%s
                """, (nome, descricao, duracao, valor, id))
                flash("Plano alterado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute("DELETE FROM PLANO WHERE ID_PLANO=%s", (id,))
                flash("Plano removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("SELECT * FROM PLANO")
    planos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("gestao_de_planos.html", planos=planos)
# -------------------- Rotas de tela de criação de tipo de treino  -------------------- #


@app.route('/treinos-padrao')
def treinos_padrao():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar os treinos padrão.", "error")
        return redirect(url_for('login'))
    return render_template('treinos_padrao.html')

# -------------------- Rotas de tela de relatorios  -------------------- #


@app.route('/relatorios')
def relatorios():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar os relatórios.", "error")
        return redirect(url_for('login'))
    return render_template('relatorios.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
