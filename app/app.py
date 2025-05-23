from validacoes import validar_cpf, validar_nome, validar_email, validar_telefone, formatar_telefone
from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import mysql.connector
import traceback
from mysql.connector import Error
from db import get_db_connection
from flask import jsonify
import traceback


app = Flask(__name__)
app.secret_key = 'secreto'


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
            "SELECT ID_User, Senha_User, Nome_User FROM USUARIO WHERE Email_user = %s", (email,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if resultado is None:
            flash("E-mail não cadastrado!", "error")
            return redirect(url_for('login'))

        id_user, senha_correta, nome = resultado
        if senha != senha_correta:
            flash("Senha incorreta!", "error")
            return redirect(url_for('login'))

        # Agora salvamos o ID corretamente na sessão
        session['usuario'] = id_user
        # opcional, pode usar para exibir "Bem-vindo, nome"
        session['nome'] = nome

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

        # Validação de CPF
        if len(cpf) > 14:
            flash("CPF inválido. Deve ter no máximo 14 caracteres.", "error")
            return redirect(url_for('cadastro'))

        if not validar_cpf(cpf):
            flash("CPF inválido. Digite um CPF real e válido.", "error")
            return redirect(url_for('cadastro'))

        # Validação de telefone (somente números e tamanho)
        import re
        telefone_numerico = re.sub(r'\D', '', telefone)
        if not telefone_numerico.isdigit() or len(telefone_numerico) not in [10, 11]:
            flash("Telefone inválido. Use um número válido com DDD.", "error")
            return redirect(url_for('cadastro'))

        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)

            # Verifica se CPF já existe
            cur.execute("SELECT * FROM USUARIO WHERE cpf_user = %s", (cpf,))
            if cur.fetchone():
                flash("CPF já cadastrado!", "error")
                cur.close()
                conn.close()
                return redirect(url_for('cadastro'))

            # Verifica se e-mail já existe
            cur.execute(
                "SELECT * FROM USUARIO WHERE Email_user = %s", (email,))
            if cur.fetchone():
                flash("E-mail já cadastrado!", "error")
                cur.close()
                conn.close()
                return redirect(url_for('cadastro'))

            # Verifica se nome está com o formato correto
            if not validar_nome(nome):
                flash("Nome inválido. O nome deve conter apenas letras.", "error")
                return redirect(url_for('cadastro'))

            # Insere novo usuário (Data_Cadastro_user será preenchido automaticamente)
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
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"Erro ao cadastrar: {str(e)}", "error")
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html', planos=planos)


# -------------------- Rotas de tela inicial logado  -------------------- #


@app.route('/inicial-logado')
def inicial_logado():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))

    nome_completo = session.get('nome', '')
    primeiro_nome = nome_completo.split()[0] if nome_completo else 'Usuário'

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

    user_id = session['usuario']  # ID_User armazenado na sessão

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT Nome_User, Email_user, Data_Nascimento, cpf_user, endereco_user,
               CEP_USER, sexo_user, status_cliente, pagou_mes_atual
        FROM usuario
        WHERE ID_User = %s
    """, (user_id,))

    usuario = cursor.fetchone()
    db.close()

    return render_template('minhaconta.html', usuario=usuario)


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
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        sexo = request.form.get('sexo')
        status = request.form.get('status_cliente')
        pagou = int(request.form.get('pagou_mes_atual') or 0)
        unidade_id = request.form.get('id_unidade')
        plano_id = request.form.get('id_plano')
        data_nascimento = request.form.get('data_nascimento')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO USUARIO (
                        Nome_User, Email_user, Senha_User, telefone_user,
                        Unidade_Prox_ID, cpf_user, logradouro_user, numero_user,
                        bairro_user, cidade_user, estado_user, CEP_USER,
                        ID_PLANO, sexo_user, status_cliente, pagou_mes_atual, Data_Nascimento
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nome, email, senha, telefone, unidade_id, cpf, logradouro, numero,
                    bairro, cidade, estado, cep, plano_id, sexo, status, pagou, data_nascimento
                ))
                flash("Usuário incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE USUARIO SET
                        Nome_User=%s,
                        Email_user=%s,
                        telefone_user=%s,
                        logradouro_user=%s,
                        numero_user=%s,
                        bairro_user=%s,
                        cidade_user=%s,
                        estado_user=%s,
                        CEP_USER=%s,
                        sexo_user=%s,
                        status_cliente=%s,
                        pagou_mes_atual=%s,
                        Unidade_Prox_ID=%s,
                        ID_PLANO=%s,
                        Data_Nascimento=%s
                    WHERE ID_User=%s
                """, (
                    nome, email, telefone, logradouro, numero, bairro, cidade, estado, cep,
                    sexo, status, pagou, unidade_id, plano_id, data_nascimento, id
                ))
                flash("Usuário atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute("DELETE FROM USUARIO WHERE ID_User = %s", (id,))
                flash("Usuário removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # Consulta
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

# -------------------- Rotas de tela de feedback  -------------------- #


@app.route('/feedbacks', methods=["POST", "GET"])
def feedbacks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        try:
            nota = request.form["nota"]
            comentario = request.form["comentario"]
            usuario_id = request.form["usuario_id"]
            unidade_id = request.form["unidade_id"]

            elogios = request.form.getlist("elogios[]")
            motivos = request.form.getlist("motivos[]")

            # Junta todas as opções selecionadas (elogios ou críticas)
            opcoes_selecionadas = elogios + motivos
            outro = ", ".join(
                opcoes_selecionadas) if opcoes_selecionadas else None

            print(
                f"Nota: {nota}, Comentário: {comentario}, Outro: {outro}, Usuario ID: {usuario_id}, Unidade ID: {unidade_id}"
            )

            cursor.execute("""
                INSERT INTO feedback (nota_user, Comentario, id_user_feedback, id_unidade, Outro)
                VALUES (%s, %s, %s, %s, %s)
            """, (nota, comentario, usuario_id, unidade_id, outro))
            connection.commit()

            flash("Feedback enviado com sucesso!", "success")
            return redirect(url_for('feedbacks'))

        except Exception as e:
            connection.rollback()
            print(f"Erro ao salvar feedback: {e}")
            flash("Erro ao enviar feedback.", "error")
            return f"Erro ao salvar no banco: {e}", 500

        finally:
            cursor.close()
            connection.close()

    else:
        try:
            cursor.execute("""
                SELECT ID_Unidades, Nome_Unidade FROM unidades
            """)
            unidades = cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar unidades: {e}")
            return f"Erro ao buscar unidades: {e}", 500

        finally:
            cursor.close()
            connection.close()

        return render_template("feedbacks.html", unidades=unidades)


# -------------------- Rotas de tela de relatorio  -------------------- #


@app.route('/relatorios', methods=["GET"])
def relatorios():
    # Conectar ao banco de dados
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Consulta: porcentagem por nota
    cursor.execute("""
        SELECT 
            (SUM(CASE WHEN nota_user = 5 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `5 estrelas`,
            (SUM(CASE WHEN nota_user = 4 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `4 estrelas`,
            (SUM(CASE WHEN nota_user = 3 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `3 estrelas`,
            (SUM(CASE WHEN nota_user = 2 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `2 estrelas`,
            (SUM(CASE WHEN nota_user = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `1 estrela`
        FROM feedback
    """)
    porcentagens = cursor.fetchone()

    # Nova consulta: comentários com nota, id_user, nome da unidade e nome da região
    cursor.execute("""
         SELECT 
        f.nota_user,
        f.Comentario,
        f.id_user_feedback,
        u.Nome_Unidade AS nome_unidade,
        r.Nome_Regiao AS nome_regiao
        FROM feedback f
        LEFT JOIN unidades u ON f.id_unidade = u.ID_Unidades
        LEFT JOIN regiao r ON u.ID_Regiao = r.ID_Regiao
        WHERE f.Comentario IS NOT NULL AND f.Comentario != ''
        ORDER BY f.nota_user;
    """)
    comentarios = cursor.fetchall()

    # Fechar conexão
    cursor.close()
    conn.close()
    print(type(comentarios))
    # Renderizar template e passar os comentários
    return render_template('relatorios.html',
                           porcentagens=porcentagens,
                           comentarios=comentarios)


# -------------------- relatorio de estrelas por unidade  API -------------------- #

@app.route("/api/feedback_porcentagem/<int:id_unidade>")
def feedback_porcentagem(id_unidade):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                SUM(CASE WHEN nota_user = 5 THEN 1 ELSE 0 END) AS cinco,
                SUM(CASE WHEN nota_user = 4 THEN 1 ELSE 0 END) AS quatro,
                SUM(CASE WHEN nota_user = 3 THEN 1 ELSE 0 END) AS tres,
                SUM(CASE WHEN nota_user = 2 THEN 1 ELSE 0 END) AS dois,
                SUM(CASE WHEN nota_user = 1 THEN 1 ELSE 0 END) AS um,
                COUNT(*) AS total
            FROM feedback
            WHERE id_unidade = %s AND nota_user BETWEEN 1 AND 5
        """, (id_unidade,))
        row = cursor.fetchone()

        total = row["total"] or 1

        porcentagens = {
            "5 estrelas": round((row["cinco"] / total) * 100, 1),
            "4 estrelas": round((row["quatro"] / total) * 100, 1),
            "3 estrelas": round((row["tres"] / total) * 100, 1),
            "2 estrelas": round((row["dois"] / total) * 100, 1),
            "1 estrela": round((row["um"] / total) * 100, 1)
        }

        return jsonify(porcentagens)

    except Exception as e:
        print("Erro ao consultar dados:")
        traceback.print_exc()
        return jsonify({"erro": "Erro ao consultar dados"}), 500

    finally:
        cursor.close()
        conn.close()


# -------------------- relatorio de estrelas por unidade  API -------------------- #

# -------------------- relatorio de estrelas por unidade -------------------- #
@app.route("/feedbackstar")
def feedbackstar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM unidades")
        unidades = cursor.fetchall()
        return render_template("feedbackstar.html", unidades=unidades)

    except Exception as e:
        print("Erro ao carregar unidades:", e)
        return "Erro ao carregar página", 500

    finally:
        cursor.close()
        conn.close()


# -------------------- relatorio de estrelas por unidade -------------------- #
# -------------------- Não mexer -------------------- #
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

# -------------------- Não mexer -------------------- #
