from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from datetime import datetime, timedelta, time

usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/minha-conta', methods=['GET', 'POST'])
def minha_conta():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash("Você precisa estar logado como aluno para acessar sua conta.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['usuario']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # --- Mensalidade: checa expiração automática ---
    cursor.execute("""
        SELECT u.*, p.duracao_meses
        FROM usuario u
        LEFT JOIN plano p ON u.ID_PLANO = p.ID_PLANO
        WHERE u.ID_User = %s
    """, (user_id,))
    usuario = cursor.fetchone()
    mensalidade_expirada = False
    try:
        if usuario and usuario.get('pagou_mes_atual') and usuario.get('data_pagamento_mes') and usuario.get('duracao_meses'):
            data_pagamento = usuario['data_pagamento_mes']
            if data_pagamento and str(data_pagamento) != 'None':
                if isinstance(data_pagamento, str):
                    data_pagamento = datetime.strptime(
                        data_pagamento, '%Y-%m-%d').date()
                meses = int(usuario['duracao_meses'])
                # Cálculo seguro de meses (sem extrapolar datas)
                try:
                    from dateutil.relativedelta import relativedelta
                    data_expira = data_pagamento + relativedelta(months=meses)
                except ImportError:
                    # Fallback: 30 dias por mês
                    data_expira = data_pagamento + timedelta(days=meses*30)
                hoje = datetime.now().date()
                if hoje >= data_expira:
                    cursor.execute(
                        "UPDATE usuario SET pagou_mes_atual=0, data_pagamento_mes=NULL WHERE ID_User=%s", (user_id,))
                    db.commit()
                    usuario['pagou_mes_atual'] = 0
                    usuario['data_pagamento_mes'] = None
                    mensalidade_expirada = True
    except Exception as e:
        # Se der erro, não expira nada, só segue
        pass

    # Processa inclusão de info_usuario
    if request.method == 'POST' and request.form.get('acao') == 'incluir_info_usuario':
        altura = request.form.get('altura') or None
        peso = request.form.get('peso') or None
        gordura = request.form.get('gordura') or None
        braquial = request.form.get('abdominal') or None
        abdominal = request.form.get('abdominal') or None
        toracico = request.form.get('toracico') or None
        cintura = request.form.get('cintura') or None
        quadril = request.form.get('quadril') or None
        imc = request.form.get('imc') or None
        obs = request.form.get('observacoes') or None
        classificacao_gordura = None
        # Buscar sexo do usuário para classificar gordura
        sexo_usuario = usuario.get('sexo_user') if usuario else None
        try:
            # Classificação de gordura corporal
            if gordura is not None and sexo_usuario is not None and gordura != '':
                try:
                    gordura_f = float(gordura)
                except ValueError:
                    gordura_f = None
                if gordura_f is not None:
                    if sexo_usuario == 'M':
                        if gordura_f < 6:
                            classificacao_gordura = 'Muito baixo'
                        elif gordura_f < 14:
                            classificacao_gordura = 'Atleta / Excelente'
                        elif gordura_f < 18:
                            classificacao_gordura = 'Bom / Fitness'
                        elif gordura_f < 25:
                            classificacao_gordura = 'Normal'
                        else:
                            classificacao_gordura = 'Alto / Obesidade'
                    elif sexo_usuario == 'F':
                        if gordura_f < 16:
                            classificacao_gordura = 'Muito baixo'
                        elif gordura_f < 24:
                            classificacao_gordura = 'Atleta / Excelente'
                        elif gordura_f < 31:
                            classificacao_gordura = 'Bom / Fitness'
                        elif gordura_f < 37:
                            classificacao_gordura = 'Normal'
                        else:
                            classificacao_gordura = 'Alto / Obesidade'
                    else:
                        classificacao_gordura = 'Não classificado'
            cursor.execute("""
                INSERT INTO info_usuario (ID_User, Altura, Peso, GorduraCorporal, Perimetro_Braquial, Perimetro_Abdominal, Perimetro_Toracico, Perimetro_Cintura, Perimetro_Quadril, IMC, Observacoes, ClassificacaoGordura)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, altura, peso, gordura, braquial, abdominal, toracico, cintura, quadril, imc, obs, classificacao_gordura))
            db.commit()
            flash('Informações físicas adicionadas com sucesso!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Erro ao adicionar informações físicas: {str(e)}', 'error')

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

    # Cálculo do próximo vencimento e nome do mês, se pago
    mes_nome = None
    proximo_vencimento = None
    if usuario and usuario.get('pagou_mes_atual') and usuario.get('data_pagamento_mes') and usuario.get('duracao_meses'):
        data_pagamento = usuario['data_pagamento_mes']
        if data_pagamento and str(data_pagamento) != 'None':
            if isinstance(data_pagamento, str):
                data_pagamento = datetime.strptime(
                    data_pagamento, '%Y-%m-%d').date()
            meses = int(usuario['duracao_meses'])
            try:
                from dateutil.relativedelta import relativedelta
                data_venc = data_pagamento + relativedelta(months=meses)
            except ImportError:
                data_venc = data_pagamento + timedelta(days=meses*30)
            proximo_vencimento = data_venc.strftime('%d/%m/%Y')
            # Mês em português
            meses_pt = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
            mes_idx = data_pagamento.month - 1
            mes_nome = meses_pt[mes_idx].capitalize(
            ) if 0 <= mes_idx < 12 else data_pagamento.strftime('%B')

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

    # Buscar dados de info_usuario
    cursor.execute("""
        SELECT * FROM info_usuario WHERE ID_User = %s ORDER BY DataMedicao DESC
    """, (user_id,))
    infos_usuario = cursor.fetchall()

    # Dropdown de datas disponíveis (agora mostra todas as datas e horários das medições)
    datas_medicao = []
    for i in infos_usuario:
        if i.get('DataMedicao'):
            data_str = i['DataMedicao'].strftime('%Y-%m-%d %H:%M:%S')
            datas_medicao.append(data_str)
    # já está em ordem decrescente por causa do ORDER BY
    datas_medicao_unicas = datas_medicao

    # Filtro por data/hora exata (GET)
    data_escolhida = request.args.get('data_medicao')
    if data_escolhida:
        infos_filtradas = [i for i in infos_usuario if i.get(
            'DataMedicao') and i['DataMedicao'].strftime('%Y-%m-%d %H:%M:%S') == data_escolhida]
    else:
        infos_filtradas = infos_usuario[:1]  # só o mais recente

    # Processa edição de conta (modal)
    if request.method == 'POST' and request.form.get('acao') == 'editar_conta':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        id_plano = request.form.get('id_plano')
        try:
            update_fields = [
                'Nome_User=%s', 'Email_user=%s', 'telefone_user=%s',
                'logradouro_user=%s', 'numero_user=%s', 'bairro_user=%s',
                'cidade_user=%s', 'estado_user=%s', 'CEP_USER=%s', 'ID_PLANO=%s'
            ]
            params = [nome, email, telefone, logradouro, numero,
                      bairro, cidade, estado, cep, id_plano, user_id]
            if senha:
                update_fields.insert(2, 'Senha_User=%s')
                params.insert(2, senha)
            cursor.execute(f"""
                UPDATE usuario SET {', '.join(update_fields)} WHERE ID_User=%s
            """, tuple(params))
            db.commit()
            flash('Dados da conta atualizados com sucesso!', 'success')
            return redirect(url_for('usuarios.minha_conta'))
        except Exception as e:
            db.rollback()
            flash(f'Erro ao atualizar dados da conta: {str(e)}', 'error')
            return redirect(url_for('usuarios.minha_conta'))

    # Buscar todos os planos para o modal de edição de conta
    cursor.execute("SELECT * FROM plano")
    planos = cursor.fetchall()

    db.close()
    return render_template('minhaconta.html', usuario=usuario, aulas=aulas, infos_usuario=infos_filtradas, datas_medicao=datas_medicao_unicas, data_escolhida=data_escolhida, mes_nome=mes_nome, proximo_vencimento=proximo_vencimento, planos=planos)


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
                    INSERT INTO usuario (
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
                    UPDATE usuario SET
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
                cursor.execute("DELETE FROM usuario WHERE ID_User = %s", (id,))
                flash("Usuário removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    plano_filtro = request.args.get('plano', '')
    status_filtro = request.args.get('status', '')
    cidade_filtro = request.args.get('cidade', '')
    bairro_filtro = request.args.get('bairro', '')
    sexo_filtro = request.args.get('sexo', '')

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

    if sexo_filtro:
        query += " AND u.sexo_user = %s"
        params.append(sexo_filtro)

    cursor.execute(query, params)
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM unidades")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM plano")
    planos = cursor.fetchall()

    cursor.execute(
        "SELECT DISTINCT cidade_user FROM usuario WHERE cidade_user IS NOT NULL AND cidade_user <> '' ORDER BY cidade_user")
    cidades = [row['cidade_user'] for row in cursor.fetchall()]

    # Buscar bairros disponíveis, filtrando pela cidade se selecionada
    if cidade_filtro:
        cursor.execute(
            "SELECT DISTINCT bairro_user FROM usuario WHERE cidade_user = %s AND bairro_user IS NOT NULL AND bairro_user <> '' ORDER BY bairro_user", (cidade_filtro,))
    else:
        cursor.execute(
            "SELECT DISTINCT bairro_user FROM usuario WHERE bairro_user IS NOT NULL AND bairro_user <> '' ORDER BY bairro_user")
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
        bairros=bairros,
        sexo_filtro=sexo_filtro
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
    # Verifica se está no prazo (até 1h antes do início), exceto para plano Unlocked
    data_treino = aula['DataTreino']
    hora_treino = aula['HoraTreino']
    # Garante que hora_treino seja datetime.time
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
    # Verifica se está no prazo (até 1h antes do início), exceto para plano Unlocked
    cursor.execute("""
        SELECT p.nome_plano FROM usuario u LEFT JOIN plano p ON u.ID_PLANO = p.ID_PLANO WHERE u.ID_User = %s
    """, (user_id,))
    row_plano = cursor.fetchone()
    nome_plano = (row_plano['nome_plano'] or '').strip(
    ).lower() if row_plano and row_plano['nome_plano'] else ''
    if nome_plano != 'unlocked':
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


@usuarios_bp.route('/inserir_info', methods=['POST'])
def inserir_info():
    from flask import request
    import mysql.connector
    from datetime import datetime
    try:
        # Coleta e validação dos dados do formulário
        user_id = int(request.form.get('ID_User', 0))
        altura = request.form.get('Altura')
        peso = request.form.get('Peso')
        gordura = request.form.get('GorduraCorporal')
        braquial = request.form.get('Perimetro_Braquial')
        abdominal = request.form.get('Perimetro_Abdominal')
        toracico = request.form.get('Perimetro_Toracico')
        cintura = request.form.get('Perimetro_Cintura')
        quadril = request.form.get('Perimetro_Quadril')
        obs = request.form.get('Observacoes')

        # Conversão para float ou None
        def to_float(val):
            try:
                return float(val)
            except (TypeError, ValueError):
                return None
        altura = to_float(altura)
        peso = to_float(peso)
        gordura = to_float(gordura)
        braquial = to_float(braquial)
        abdominal = to_float(abdominal)
        toracico = to_float(toracico)
        cintura = to_float(cintura)
        quadril = to_float(quadril)

        # Calcula IMC se possível
        imc = None
        if altura and peso and altura > 0:
            imc = round(peso / (altura ** 2), 2)

        # Buscar o sexo do usuário
        from db import get_db_connection
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT sexo_user FROM usuario WHERE ID_User = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            sexo_usuario = user_data['sexo_user']
        else:
            sexo_usuario = None  # Caso não encontre, não classifica

        # Classificar gordura corporal
        classificacao_gordura = None
        if gordura is not None and sexo_usuario is not None:
            if sexo_usuario == 'M':
                if gordura < 6:
                    classificacao_gordura = 'Muito baixo'
                elif gordura < 14:
                    classificacao_gordura = 'Atleta / Excelente'
                elif gordura < 18:
                    classificacao_gordura = 'Bom / Fitness'
                elif gordura < 25:
                    classificacao_gordura = 'Normal'
                else:
                    classificacao_gordura = 'Alto / Obesidade'
            elif sexo_usuario == 'F':
                if gordura < 16:
                    classificacao_gordura = 'Muito baixo'
                elif gordura < 24:
                    classificacao_gordura = 'Atleta / Excelente'
                elif gordura < 31:
                    classificacao_gordura = 'Bom / Fitness'
                elif gordura < 37:
                    classificacao_gordura = 'Normal'
                else:
                    classificacao_gordura = 'Alto / Obesidade'
            else:
                classificacao_gordura = 'Não classificado'

        # Inserir no banco de dados
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO info_usuario (
                ID_User, Altura, Peso, GorduraCorporal, Perimetro_Braquial, Perimetro_Abdominal, Perimetro_Toracico,
                Perimetro_Cintura, Perimetro_Quadril, IMC, ClassificacaoGordura, Observacoes, DataMedicao
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            user_id, altura, peso, gordura, braquial, abdominal, toracico, cintura, quadril,
            imc, classificacao_gordura, obs
        ))

        db.commit()
        cursor.close()
        db.close()
        return 'Informações físicas inseridas com sucesso!'
    except Exception as e:
        return f'Erro ao inserir informações físicas: {str(e)}'


@usuarios_bp.route('/pagar-mensalidade', methods=['POST'])
def pagar_mensalidade():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash("Você precisa estar logado como aluno para pagar a mensalidade.", "error")
        return redirect(url_for('auth.login'))
    user_id = session['usuario']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "UPDATE usuario SET pagou_mes_atual=1, data_pagamento_mes=CURDATE() WHERE ID_User=%s", (user_id,))
    db.commit()
    db.close()
    flash('Mensalidade paga com sucesso! Aproveite seu plano.', 'success')
    return redirect(url_for('usuarios.minha_conta'))
