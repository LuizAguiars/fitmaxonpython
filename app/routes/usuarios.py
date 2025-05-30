from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from datetime import datetime, timedelta, time

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/minha-conta')
def minha_conta():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash("Você precisa estar logado como aluno para acessar sua conta.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['usuario']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Nome_User, Email_user, Data_Nascimento, cpf_user, CEP_USER, sexo_user, status_cliente, pagou_mes_atual,
               logradouro_user, numero_user, bairro_user, cidade_user, estado_user
        FROM usuario
        WHERE ID_User = %s
    """, (user_id,))
    usuario = cursor.fetchone()

    # Monta endereço formatado
    if usuario:
        partes = []
        if usuario.get('logradouro_user'):
            partes.append(usuario['logradouro_user'])
        if usuario.get('numero_user'):
            partes.append(usuario['numero_user'])
        if usuario.get('bairro_user'):
            partes.append(usuario['bairro_user'])
        if usuario.get('cidade_user'):
            partes.append(usuario['cidade_user'])
        if usuario.get('estado_user'):
            partes.append(usuario['estado_user'])
        usuario['endereco_formatado'] = ', '.join(partes) if partes else None

    # Buscar aulas agendadas e concluídas
    cursor.execute("""
        SELECT a.idAgendar_Treino, a.DataTreino, a.HoraTreino, t.nome_tipo_treino, p.Nome_Personal, a.status
        FROM agendar_treino a
        JOIN tipo_de_treino t ON a.ID_Tipodetreino = t.idtipo_de_treino
        JOIN personal p ON a.ID_Personal = p.ID_Personal
        WHERE a.ID_usuario = %s
        ORDER BY a.DataTreino DESC, a.HoraTreino DESC
    """, (user_id,))
    aulas = cursor.fetchall()
    db.close()
    return render_template('minhaconta.html', usuario=usuario, aulas=aulas)


# Adicionando lógica para filtrar por plano e status
@usuarios_bp.route('/gestao-usuarios', methods=['GET', 'POST'])
def gestao_usuarios():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash("Você precisa estar logado como aluno para acessar a gestão de usuários.", "error")
        return redirect(url_for('auth.login'))

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

    plano_filtro = request.args.get('plano', '')
    status_filtro = request.args.get('status', '')
    cidade_filtro = request.args.get('cidade', '')
    bairro_filtro = request.args.get('bairro', '')

    query = """
        SELECT u.*, un.Nome_Unidade, p.nome_plano
        FROM USUARIO u
        LEFT JOIN UNIDADES un ON u.Unidade_Prox_ID = un.ID_Unidades
        LEFT JOIN PLANO p ON u.ID_PLANO = p.ID_PLANO
        WHERE 1=1
    """
    params = []

    if plano_filtro:
        query += " AND u.ID_PLANO = %s"
        params.append(plano_filtro)

    if status_filtro:
        query += " AND u.status_cliente = %s"
        params.append(status_filtro)

    if cidade_filtro:
        query += " AND u.cidade_user = %s"
        params.append(cidade_filtro)

    if bairro_filtro:
        query += " AND u.bairro_user = %s"
        params.append(bairro_filtro)

    cursor.execute(query, params)
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM PLANO")
    planos = cursor.fetchall()

    cursor.execute("SELECT DISTINCT cidade_user FROM USUARIO WHERE cidade_user IS NOT NULL AND cidade_user <> '' ORDER BY cidade_user")
    cidades = [row['cidade_user'] for row in cursor.fetchall()]

    # Buscar bairros disponíveis, filtrando pela cidade se selecionada
    if cidade_filtro:
        cursor.execute("SELECT DISTINCT bairro_user FROM USUARIO WHERE cidade_user = %s AND bairro_user IS NOT NULL AND bairro_user <> '' ORDER BY bairro_user", (cidade_filtro,))
    else:
        cursor.execute("SELECT DISTINCT bairro_user FROM USUARIO WHERE bairro_user IS NOT NULL AND bairro_user <> '' ORDER BY bairro_user")
    bairros = [row['bairro_user'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        'gestao_usuarios.html',
        usuarios=usuarios,
        unidades=unidades,
        planos=planos,
        plano_filtro=plano_filtro,
        status_filtro=status_filtro,
        cidade_filtro=cidade_filtro,
        bairro_filtro=bairro_filtro,
        cidades=cidades,
        bairros=bairros
    )


@usuarios_bp.route('/minhas-aulas', methods=['GET'])
def minhas_aulas():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Filtros GET
    ano = request.args.get('ano')
    mes = request.args.get('mes')
    tipo = request.args.get('tipo')
    status = request.args.get('status')
    try:
        per_page = int(request.args.get('per_page', 8))  # padrão agora é 8
    except ValueError:
        per_page = 8
    per_page = max(4, min(per_page, 16))
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    offset = (page - 1) * per_page

    # Monta a query base
    query_base = """
        FROM agendar_treino a
        JOIN tipo_de_treino t ON a.ID_Tipodetreino = t.idtipo_de_treino
        JOIN personal p ON a.ID_Personal = p.ID_Personal
        WHERE a.ID_usuario = %s
    """
    params = [session['usuario']]

    if status:
        query_base += " AND a.status = %s"
        params.append(status)
    if ano:
        query_base += " AND YEAR(a.DataTreino) = %s"
        params.append(int(ano))
    if mes:
        query_base += " AND MONTH(a.DataTreino) = %s"
        params.append(int(mes))
    if tipo:
        query_base += " AND a.ID_Tipodetreino = %s"
        params.append(int(tipo))

    # Conta total de registros para paginação
    cursor.execute(f"SELECT COUNT(*) as total {query_base}", tuple(params))
    total = cursor.fetchone()['total']
    total_pages = max(1, (total + per_page - 1) // per_page)

    # Busca as aulas paginadas
    query = f"""
        SELECT a.*, t.nome_tipo_treino, p.Nome_Personal
        {query_base}
        ORDER BY a.DataTreino DESC, a.HoraTreino DESC
        LIMIT %s OFFSET %s
    """
    params_paged = params + [per_page, offset]
    cursor.execute(query, tuple(params_paged))
    aulas = cursor.fetchall()

    # Buscar todos os tipos de treino para o filtro
    cursor.execute(
        "SELECT idtipo_de_treino, nome_tipo_treino FROM tipo_de_treino")
    tipos_treino = cursor.fetchall()

    # Buscar anos disponíveis para filtro
    cursor.execute(
        "SELECT DISTINCT YEAR(DataTreino) as ano FROM agendar_treino WHERE ID_usuario = %s ORDER BY ano DESC", (session['usuario'],))
    anos_disponiveis = [row['ano'] for row in cursor.fetchall()]

    conn.close()
    return render_template(
        'minhas_aulas.html',
        aulas=aulas,
        tipos_treino=tipos_treino,
        anos_disponiveis=anos_disponiveis,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total=total
    )


@usuarios_bp.route('/cancelar-aula', methods=['POST'])
def cancelar_aula():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash("Você precisa estar logado como aluno para cancelar uma aula.", "error")
        return redirect(url_for('auth.login'))
    user_id = session['usuario']
    id_agenda = request.form.get('id_agenda')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT ID_usuario, DataTreino, HoraTreino, status FROM agendar_treino WHERE idAgendar_Treino = %s
    """, (id_agenda,))
    aula = cursor.fetchone()
    if not aula or aula['ID_usuario'] != user_id:
        db.close()
        flash('Aula não encontrada ou não pertence a você.', 'error')
        return redirect(url_for('usuarios.minhas_aulas'))
    if aula['status'] != 'Agendado':
        db.close()
        flash('Só é possível cancelar aulas agendadas.', 'error')
        return redirect(url_for('usuarios.minhas_aulas'))
    # Verifica se está no prazo (até 1h antes do início)
    data_treino = aula['DataTreino']
    hora_treino = aula['HoraTreino']
    if isinstance(hora_treino, str):
        hora_treino = datetime.strptime(hora_treino, '%H:%M:%S').time() if len(
            hora_treino) > 5 else datetime.strptime(hora_treino, '%H:%M').time()
    elif hasattr(hora_treino, 'seconds'):
        total_seconds = hora_treino.seconds
        horas = total_seconds // 3600
        minutos = (total_seconds // 60) % 60
        hora_treino = time(hour=horas, minute=minutos)
    datahora_treino = datetime.combine(data_treino, hora_treino)
    agora = datetime.now()
    if agora > datahora_treino - timedelta(hours=1):
        db.close()
        flash('Só é possível cancelar aulas até 1 hora antes do início.', 'error')
        return redirect(url_for('usuarios.minhas_aulas'))
    cursor.execute(
        "UPDATE agendar_treino SET status = 'Cancelado' WHERE idAgendar_Treino = %s", (id_agenda,))
    db.commit()
    db.close()
    flash('Aula cancelada com sucesso!', 'success')
    return redirect(url_for('usuarios.minhas_aulas'))
