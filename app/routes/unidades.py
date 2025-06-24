from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

unidades_bp = Blueprint('unidades', __name__)


@unidades_bp.route('/gestao-unidades', methods=['GET', 'POST'])
def gerenciar_unidade():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de unidades.", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --- TRATAMENTO DE INCLUSÃO DE UNIDADE ---
    if request.method == 'POST' and request.form.get('acao') == 'incluir':
        nome = request.form.get('nome')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        capacidade = request.form.get('capacidade')
        fone = request.form.get('fone')
        cnpj = request.form.get('cnpj')
        email = request.form.get('email')
        horario_funcionamento_id = request.form.get('horario_funcionamento_id')
        try:
            cursor.execute("""
                INSERT INTO unidades (Nome_Unidade, logradouro_unidade, numero_unidade, bairro_unidade, cidade_unidade, estado_unidade, cep_unidade, Capacidade, Fone, CNPJ, Email, Horario_Funcionamento_ID, Ativa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, (nome, logradouro, numero, bairro, cidade, estado, cep, capacidade, fone, cnpj, email, horario_funcionamento_id))
            conn.commit()
            flash('Unidade incluída com sucesso!', 'success')
            return redirect(url_for('unidades.gerenciar_unidade'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao incluir unidade: {str(e)}', 'error')
            return redirect(url_for('unidades.gerenciar_unidade'))

    # --- TRATAMENTO DE EDIÇÃO DE UNIDADE ---
    if request.method == 'POST' and request.form.get('acao') == 'editar':
        id_unidade = request.form.get('id')
        nome = request.form.get('nome')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        capacidade = request.form.get('capacidade')
        fone = request.form.get('fone')
        cnpj = request.form.get('cnpj')
        email = request.form.get('email')
        horario_funcionamento_id = request.form.get('horario_funcionamento_id')
        try:
            cursor.execute("""
                UPDATE unidades SET Nome_Unidade=%s, logradouro_unidade=%s, numero_unidade=%s, bairro_unidade=%s, cidade_unidade=%s, estado_unidade=%s, cep_unidade=%s, Capacidade=%s, Fone=%s, CNPJ=%s, Email=%s, Horario_Funcionamento_ID=%s
                WHERE ID_Unidades=%s
            """, (nome, logradouro, numero, bairro, cidade, estado, cep, capacidade, fone, cnpj, email, horario_funcionamento_id, id_unidade))
            conn.commit()
            flash('Unidade atualizada com sucesso!', 'success')
            return redirect(url_for('unidades.gerenciar_unidade'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao atualizar unidade: {str(e)}', 'error')
            return redirect(url_for('unidades.gerenciar_unidade'))

    # --- TRATAMENTO DE DESATIVAÇÃO DE UNIDADE ---
    if request.method == 'POST' and request.form.get('acao') == 'desativar':
        id_unidade = request.form.get('id')
        try:
            # Verificar se há usuários vinculados à unidade
            cursor.execute(
                "SELECT COUNT(*) as total FROM usuario WHERE Unidade_Prox_ID = %s", (id_unidade,))
            usuarios_vinculados = cursor.fetchone()['total']

            # Verificar se há personais vinculados à unidade
            cursor.execute(
                "SELECT COUNT(*) as total FROM personal WHERE ID_Unidade = %s", (id_unidade,))
            personais_vinculados = cursor.fetchone()['total']

            # Verificar se há equipamentos vinculados à unidade
            cursor.execute(
                "SELECT COUNT(*) as total FROM equipamentos WHERE ID_unidade_equipamento = %s", (id_unidade,))
            equipamentos_vinculados = cursor.fetchone()['total']

            # Verificar se há aulas agendadas para a unidade
            cursor.execute(
                "SELECT COUNT(*) as total FROM agendar_treino WHERE ID_Unidade_Treino = %s AND status = 'Agendado'", (id_unidade,))
            aulas_agendadas = cursor.fetchone()['total']

            # Verificar se existem vínculos que impedem a desativação
            impedimentos = []
            if usuarios_vinculados > 0:
                impedimentos.append(f"{usuarios_vinculados} usuário(s)")
            if personais_vinculados > 0:
                impedimentos.append(f"{personais_vinculados} personal(is)")
            if equipamentos_vinculados > 0:
                impedimentos.append(
                    f"{equipamentos_vinculados} equipamento(s)")
            if aulas_agendadas > 0:
                impedimentos.append(f"{aulas_agendadas} aula(s) agendada(s)")

            if impedimentos:
                motivos = ", ".join(impedimentos)
                flash(
                    f'Não é possível desativar a unidade. Ainda possui: {motivos}. Remova ou transfira esses vínculos antes de desativar a unidade.', 'error')
                # Se não há impedimentos, desativar a unidade
                return redirect(url_for('unidades.gerenciar_unidade'))
            cursor.execute(
                "UPDATE unidades SET Ativa = 0 WHERE ID_Unidades = %s", (id_unidade,))
            conn.commit()
            flash('Unidade desativada com sucesso!', 'success')
            return redirect(url_for('unidades.gerenciar_unidade'))

        except Exception as e:
            conn.rollback()
            flash(f'Erro ao desativar unidade: {str(e)}', 'error')
            return redirect(url_for('unidades.gerenciar_unidade'))

    # --- TRATAMENTO DE REATIVAÇÃO DE UNIDADE ---
    if request.method == 'POST' and request.form.get('acao') == 'reativar':
        id_unidade = request.form.get('id')
        try:
            cursor.execute(
                "UPDATE unidades SET Ativa = 1 WHERE ID_Unidades = %s", (id_unidade,))
            conn.commit()
            flash('Unidade reativada com sucesso!', 'success')
            return redirect(url_for('unidades.gerenciar_unidade'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao reativar unidade: {str(e)}', 'error')
            return redirect(url_for('unidades.gerenciar_unidade'))

    # Filtros
    cidade_filtro = request.args.get('cidade', '')
    bairro_filtro = request.args.get('bairro', '')
    capacidade_filtro = request.args.get('capacidade', '')
    status_filtro = request.args.get(
        'status', 'ativo')  # Padrão: apenas ativas

    # Construir query base considerando o filtro de status
    if status_filtro == 'inativo':
        query = "SELECT u.*, h.Descricao_Horario FROM unidades u LEFT JOIN horarios_funcionamento h ON u.Horario_Funcionamento_ID = h.ID_Horario WHERE Ativa=0"
    elif status_filtro == 'todos':
        query = "SELECT u.*, h.Descricao_Horario FROM unidades u LEFT JOIN horarios_funcionamento h ON u.Horario_Funcionamento_ID = h.ID_Horario WHERE 1=1"
    else:  # ativo ou padrão
        query = "SELECT u.*, h.Descricao_Horario FROM unidades u LEFT JOIN horarios_funcionamento h ON u.Horario_Funcionamento_ID = h.ID_Horario WHERE Ativa=1"
    params = []

    if cidade_filtro:
        query += " AND cidade_unidade = %s"
        params.append(cidade_filtro)

    if bairro_filtro:
        query += " AND bairro_unidade = %s"
        params.append(bairro_filtro)

    if capacidade_filtro and capacidade_filtro.lower() != 'todas':
        query += " AND Capacidade = %s"
        params.append(capacidade_filtro)
    else:
        capacidade_filtro = None    # Paginação
    itens_por_pagina = int(request.args.get('itensPorPagina', 25))
    pagina = int(request.args.get('pagina', 1))
    offset = (pagina - 1) * itens_por_pagina

    query += " LIMIT %s OFFSET %s"
    params.extend([itens_por_pagina, offset])

    cursor.execute(query, params)
    unidades = cursor.fetchall()

    # Contar total de unidades considerando o filtro de status
    count_query = "SELECT COUNT(*) as total FROM unidades u WHERE "
    if status_filtro == 'inativo':
        count_query += "Ativa=0"
    elif status_filtro == 'todos':
        count_query += "1=1"
    else:  # ativo ou padrão
        count_query += "Ativa=1"
      # Aplicar os mesmos filtros da query principal
    count_params = []
    if cidade_filtro:
        count_query += " AND cidade_unidade = %s"
        count_params.append(cidade_filtro)
    if bairro_filtro:
        count_query += " AND bairro_unidade = %s"
        count_params.append(bairro_filtro)
    if capacidade_filtro and capacidade_filtro.lower() != 'todas':
        count_query += " AND Capacidade = %s"
        count_params.append(capacidade_filtro)

    cursor.execute(count_query, count_params)
    total_unidades = cursor.fetchone()['total']
    total_paginas = (total_unidades + itens_por_pagina - 1) // itens_por_pagina

    cursor.execute("SELECT * FROM horarios_funcionamento")
    horarios = cursor.fetchall()

    # Determinar condição de status para filtros
    status_condition = ""
    if status_filtro == 'inativo':
        status_condition = "Ativa=0"
    elif status_filtro == 'todos':
        status_condition = "1=1"
    else:  # ativo ou padrão
        status_condition = "Ativa=1"

    # Buscar cidades disponíveis considerando o status atual
    cursor.execute(
        f"SELECT DISTINCT cidade_unidade FROM unidades WHERE {status_condition} AND cidade_unidade IS NOT NULL AND cidade_unidade <> '' ORDER BY cidade_unidade")
    cidades_disponiveis = [row['cidade_unidade'] for row in cursor.fetchall()]

    # Buscar bairros disponíveis, filtrando pela cidade se selecionada, considerando o status atual
    if cidade_filtro:
        cursor.execute(
            f"SELECT DISTINCT bairro_unidade FROM unidades WHERE {status_condition} AND cidade_unidade = %s AND bairro_unidade IS NOT NULL AND bairro_unidade <> '' ORDER BY bairro_unidade", (cidade_filtro,))
    else:
        cursor.execute(
            f"SELECT DISTINCT bairro_unidade FROM unidades WHERE {status_condition} AND bairro_unidade IS NOT NULL AND bairro_unidade <> '' ORDER BY bairro_unidade")
    bairros_disponiveis = [row['bairro_unidade'] for row in cursor.fetchall()]

    # Buscar capacidades disponíveis considerando o status atual
    cursor.execute(
        f"SELECT DISTINCT Capacidade FROM unidades WHERE {status_condition} AND Capacidade IS NOT NULL AND Capacidade <> '' ORDER BY Capacidade")
    capacidades_disponiveis = [row['Capacidade'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template(
        'gestao_unidades.html',
        unidades=unidades,
        horarios=horarios,
        total_paginas=total_paginas,
        pagina=pagina,
        itens_por_pagina=itens_por_pagina,
        cidades_disponiveis=cidades_disponiveis,
        bairros_disponiveis=bairros_disponiveis,
        cidade_filtro=cidade_filtro,
        bairro_filtro=bairro_filtro,
        capacidades_disponiveis=capacidades_disponiveis,
        status_filtro=status_filtro
    )
