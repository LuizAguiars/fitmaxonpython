from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

equipamentos_bp = Blueprint('equipamentos', __name__)


@equipamentos_bp.route('/gestao-equipamentos', methods=['GET', 'POST'])
def gestao_equipamentos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de equipamentos.", "error")
        return redirect(url_for('auth.login'))

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
                    INSERT INTO equipamentos
                    (Nome_Equipamento, descricao_equipamentos, data_de_compra,
                     ID_unidade_equipamento, id_status_do_equipamento, idtipo_equipamento)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo))
                flash("Equipamento incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE equipamentos
                    SET Nome_Equipamento=%s, descricao_equipamentos=%s, data_de_compra=%s,
                        ID_unidade_equipamento=%s, id_status_do_equipamento=%s, idtipo_equipamento=%s
                    WHERE id_equipamentos=%s
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo, id))
                flash("Equipamento atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM equipamentos WHERE id_equipamentos = %s", (id,))
                flash("Equipamento removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    unidade_filtro = request.args.get('unidade', '')
    status_filtro = request.args.get('status', '')
    tipo_filtro = request.args.get('tipo', '')

    query = """
        SELECT e.*, u.Nome_Unidade, s.status_do_Equipamento, t.nome_tipo_equipamento
        FROM equipamentos e
        LEFT JOIN UNIDADES u ON e.ID_unidade_equipamento = u.ID_Unidades
        LEFT JOIN status_dos_Equipamentos s ON e.id_status_do_equipamento = s.idstatus_dos_Equipamentos
        LEFT JOIN tipo_equipamento t ON e.idtipo_equipamento = t.idtipo_equipamento
        WHERE 1=1
    """
    params = []

    if unidade_filtro:
        query += " AND e.ID_unidade_equipamento = %s"
        params.append(unidade_filtro)

    if status_filtro:
        query += " AND e.id_status_do_equipamento = %s"
        params.append(status_filtro)

    if tipo_filtro:
        query += " AND e.idtipo_equipamento = %s"
        params.append(tipo_filtro)

    cursor.execute(query, params)
    equipamentos = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM status_dos_equipamentos")
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
        tipos_equipamento=tipos_equipamento,
        unidade_filtro=unidade_filtro,
        status_filtro=status_filtro,
        tipo_filtro=tipo_filtro
    )


@equipamentos_bp.route('/relatorio-equipamentos', methods=['GET'])
def relatorio_equipamentos():
    if 'usuario' not in session:
        flash(
            "Você precisa estar logado para acessar o relatório de equipamentos.", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar unidades para o filtro
    cursor.execute("SELECT id_unidades, nome_unidade FROM unidades")
    unidades = cursor.fetchall()

    unidade_id = request.args.get('unidade_id', '')
    unidade_nome = None
    filtro_unidade = ''
    params = []
    if unidade_id:
        filtro_unidade = 'WHERE e.ID_unidade_equipamento = %s'
        params.append(unidade_id)
        unidade_nome = next((u['Nome_Unidade'] for u in unidades if str(
            u['ID_Unidades']) == unidade_id), None)

    # Relatório: Equipamento mais usado e menos usado
    cursor.execute(f"""
        SELECT e.ID_equipamentos, e.Nome_Equipamento, COALESCE(SUM(ue.tempo_utilizado_minutos),0) as total_minutos
        FROM equipamentos e
        LEFT JOIN uso_equipamentos ue ON e.ID_equipamentos = ue.id_equipamento
        {filtro_unidade}
        GROUP BY e.ID_equipamentos
    """, params)
    uso_equipamentos = cursor.fetchall()

    mais_usado = menos_usado = None
    if uso_equipamentos:
        mais_usado = max(uso_equipamentos, key=lambda x: x['total_minutos'])
        menos_usado = min(uso_equipamentos, key=lambda x: x['total_minutos'])

    # Relatório: Todos os equipamentos e seus totais de uso
    equipamentos_uso = [
        {
            'nome': eq['Nome_Equipamento'],
            'total_minutos': eq['total_minutos'],
            'total_horas': round((eq['total_minutos'] or 0) / 60, 2)
        }
        for eq in uso_equipamentos
    ]

    # Buscar horários de funcionamento das unidades
    horarios_unidade = {}
    cursor.execute(
        "SELECT id_unidades, horario_funcionamento_id FROM unidades")
    for row in cursor.fetchall():
        horarios_unidade[row['ID_Unidades']] = row['Horario_Funcionamento_ID']

    horarios_funcionamento = {}
    if unidade_id and horarios_unidade.get(int(unidade_id)):
        cursor.execute("SELECT * FROM horarios_funcionamento WHERE id_horario = %s",
                       (horarios_unidade[int(unidade_id)],))
        horario = cursor.fetchone()
        if horario:
            horarios_funcionamento = horario

    dia_semana = request.args.get('dia_semana', '')

    # Mapear nomes para índices de dias (1=Segunda, ..., 7=Domingo)
    dias_map = {
        'Segunda': 1, 'Terca': 2, 'Quarta': 3, 'Quinta': 4, 'Sexta': 5, 'Sabado': 6, 'Domingo': 7
    }
    dia_idx = dias_map.get(dia_semana)

    # Ajustar filtro de uso para o dia da semana, se selecionado
    filtro_dia = ''
    params_dia = list(params)
    if dia_idx:
        filtro_dia = ' AND DAYOFWEEK(ue.data_uso) = %s'
        # DAYOFWEEK: 1=Domingo, 2=Segunda, ..., 7=Sábado (MySQL)
        # Ajustar para compatibilidade com o mapeamento
        mysql_idx = (dia_idx % 7) + 1  # Segunda=2, ..., Domingo=1
        params_dia.append(mysql_idx)

    # Buscar uso de equipamentos por dia da semana
    cursor.execute(f'''
        SELECT e.ID_equipamentos, e.Nome_Equipamento, COALESCE(SUM(ue.tempo_utilizado_minutos),0) as total_minutos
        FROM equipamentos e
        LEFT JOIN uso_equipamentos ue ON e.ID_equipamentos = ue.id_equipamento
        {'WHERE' if filtro_unidade or filtro_dia else ''}
        {' AND '.join(filter(None, [filtro_unidade.replace('WHERE', ''), filtro_dia.replace('AND', '')]))}
        GROUP BY e.ID_equipamentos
    ''', params_dia)
    uso_equipamentos = cursor.fetchall()

    mais_usado = menos_usado = None
    if uso_equipamentos:
        mais_usado = max(uso_equipamentos, key=lambda x: x['total_minutos'])
        menos_usado = min(uso_equipamentos, key=lambda x: x['total_minutos'])

    equipamentos_uso = [
        {
            'nome': eq['Nome_Equipamento'],
            'total_minutos': eq['total_minutos'],
            'total_horas': round((eq['total_minutos'] or 0) / 60, 2)
        }
        for eq in uso_equipamentos
    ]

    # Buscar horários de funcionamento da unidade para o dia selecionado
    horarios_funcionamento_dia = None
    if unidade_id and horarios_unidade.get(int(unidade_id)):
        cursor.execute("SELECT * FROM horarios_funcionamento WHERE id_horario = %s",
                       (horarios_unidade[int(unidade_id)],))
        horario = cursor.fetchone()
        if horario and dia_idx:
            inicio = horario.get(f'inicio_dia{dia_idx}')
            fim = horario.get(f'fim_dia{dia_idx}')
            if inicio and fim:
                h1, m1 = map(int, str(inicio).split(':'))
                h2, m2 = map(int, str(fim).split(':'))
                minutos_disponiveis = (h2*60+m2) - (h1*60+m1)
                horarios_funcionamento_dia = minutos_disponiveis

    # Tempo ocioso dos equipamentos para o dia filtrado
    ociosidade = []
    if horarios_funcionamento_dia is not None:
        for eq in uso_equipamentos:
            tempo_ocioso = horarios_funcionamento_dia - \
                (eq['total_minutos'] or 0)
            ociosidade.append({
                'nome': eq['Nome_Equipamento'],
                'minutos_ocioso': max(0, tempo_ocioso),
                'horas_ocioso': round(max(0, tempo_ocioso)/60, 2)
            })
    else:
        # fallback: calcula como antes (todos os dias)
        # Exemplo: calcula minutos disponíveis por dia
        minutos_disponiveis = 0
        for i in range(1, 8):
            inicio = horarios_funcionamento.get(f'inicio_dia{i}')
            fim = horarios_funcionamento.get(f'fim_dia{i}')
            if inicio and fim:
                h1, m1 = map(int, str(inicio).split(':'))
                h2, m2 = map(int, str(fim).split(':'))
                minutos_disponiveis += (h2*60+m2) - (h1*60+m1)
        for eq in uso_equipamentos:
            tempo_ocioso = minutos_disponiveis - (eq['total_minutos'] or 0)
            ociosidade.append({
                'nome': eq['Nome_Equipamento'],
                'minutos_ocioso': max(0, tempo_ocioso),
                'horas_ocioso': round(max(0, tempo_ocioso)/60, 2)
            })

    equipamento_id = request.args.get('equipamento_id', '')

    # Se um equipamento for selecionado, calcular ociosidade por dia da semana
    ociosidade_por_dia = []
    if equipamento_id:
        # Buscar ID do equipamento pelo nome
        cursor.execute(
            "SELECT ID_equipamentos FROM equipamentos WHERE Nome_Equipamento = %s", (equipamento_id,))
        row = cursor.fetchone()
        if row:
            eq_id = row['ID_equipamentos']
            # Buscar horários de funcionamento da unidade
            if unidade_id and horarios_unidade.get(int(unidade_id)):
                cursor.execute("SELECT * FROM horarios_funcionamento WHERE id_horario = %s",
                               (horarios_unidade[int(unidade_id)],))
                horario = cursor.fetchone()
                for i in range(1, 8):
                    inicio = horario.get(f'inicio_dia{i}')
                    fim = horario.get(f'fim_dia{i}')
                    if inicio and fim:
                        h1, m1 = map(int, str(inicio).split(':'))
                        h2, m2 = map(int, str(fim).split(':'))
                        minutos_disponiveis = (h2*60+m2) - (h1*60+m1)
                        # Buscar tempo de uso real nesse dia da semana
                        # DAYOFWEEK: 1=Domingo, 2=Segunda, ..., 7=Sábado
                        mysql_idx = (i % 7) + 1
                        cursor.execute('''
                            SELECT COALESCE(SUM(tempo_utilizado_minutos),0) as total_minutos
                            FROM uso_equipamentos
                            WHERE id_equipamento = %s
                            AND DAYOFWEEK(data_uso) = %s
                        ''', (eq_id, mysql_idx))
                        total_minutos = cursor.fetchone()['total_minutos']
                        tempo_ocioso = minutos_disponiveis - \
                            (total_minutos or 0)
                        ociosidade_por_dia.append({
                            'dia': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'][i-1],
                            'minutos_ocioso': max(0, tempo_ocioso),
                            'horas_ocioso': round(max(0, tempo_ocioso)/60, 2),
                            'minutos_uso': total_minutos,
                            'horas_uso': round((total_minutos or 0)/60, 2),
                            'minutos_disponiveis': minutos_disponiveis,
                            'horas_disponiveis': round(minutos_disponiveis/60, 2)
                        })

    # Novo filtro: mês (formato yyyy-mm)
    mes = request.args.get('mes', '')
    filtro_mes = ''
    params_mes = list(params)
    if mes:
        filtro_mes = ' AND DATE_FORMAT(ag.DataTreino, "%Y-%m") = %s'
        params_mes.append(mes)

    # Relatório: Equipamento mais usado e menos usado (com filtro de mês)
    cursor.execute(f'''
        SELECT e.ID_equipamentos, e.Nome_Equipamento, COALESCE(SUM(ue.tempo_utilizado_minutos),0) as total_minutos
        FROM equipamentos e
        LEFT JOIN uso_equipamentos ue ON e.ID_equipamentos = ue.id_equipamento
        LEFT JOIN agendar_treino ag ON ue.id_treino_agendado = ag.idAgendar_Treino
        {f"WHERE 1=1 {f'AND e.ID_unidade_equipamento = %s' if unidade_id else ''} {filtro_mes}"}
        GROUP BY e.ID_equipamentos
    ''', params_mes)
    uso_equipamentos = cursor.fetchall()

    mais_usado = menos_usado = None
    if uso_equipamentos:
        mais_usado = max(uso_equipamentos, key=lambda x: x['total_minutos'])
        menos_usado = min(uso_equipamentos, key=lambda x: x['total_minutos'])

    equipamentos_uso = [
        {
            'nome': eq['Nome_Equipamento'],
            'total_minutos': eq['total_minutos'],
            'total_horas': round((eq['total_minutos'] or 0) / 60, 2)
        }
        for eq in uso_equipamentos
    ]

    # Buscar horários de funcionamento da unidade
    horarios_unidade = {}
    cursor.execute(
        "SELECT id_unidades, horario_funcionamento_id FROM unidades")
    for row in cursor.fetchall():
        horarios_unidade[row['ID_Unidades']] = row['Horario_Funcionamento_ID']

    horarios_funcionamento = {}
    if unidade_id and horarios_unidade.get(int(unidade_id)):
        cursor.execute("SELECT * FROM horarios_funcionamento WHERE id_horario = %s",
                       (horarios_unidade[int(unidade_id)],))
        horario = cursor.fetchone()
        if horario:
            horarios_funcionamento = horario

    # Relatório de ociosidade por equipamento no mês
    from datetime import datetime, timedelta
    import calendar
    ociosidade_mensal = []
    if mes and horarios_funcionamento:
        ano, mes_num = map(int, mes.split('-'))
        dias_no_mes = calendar.monthrange(ano, mes_num)[1]
        for eq in uso_equipamentos:  # Corrigido: usar uso_equipamentos
            total_ocioso = 0
            for dia in range(1, dias_no_mes+1):
                data_dia = datetime(ano, mes_num, dia)
                dia_semana = data_dia.isoweekday()  # 1=Segunda ... 7=Domingo
                # Buscar horário funcionamento do dia
                inicio = horarios_funcionamento.get(f'inicio_dia{dia_semana}')
                fim = horarios_funcionamento.get(f'fim_dia{dia_semana}')
                if not inicio or not fim:
                    continue  # unidade fechada
                h1, m1 = map(int, str(inicio).split(':'))
                h2, m2 = map(int, str(fim).split(':'))
                inicio_dia = data_dia.replace(hour=h1, minute=m1, second=0)
                fim_dia = data_dia.replace(hour=h2, minute=m2, second=0)
                # Buscar todos os usos do equipamento nesse dia
                cursor.execute('''
                    SELECT ag.HoraTreino, ue.tempo_utilizado_minutos
                    FROM agendar_treino ag
                    JOIN uso_equipamentos ue ON ag.idAgendar_Treino = ue.id_treino_agendado
                    WHERE ag.DataTreino = %s AND ue.id_equipamento = %s
                    ORDER BY ag.HoraTreino ASC
                ''', (data_dia.strftime('%Y-%m-%d'), eq['ID_equipamentos']))
                usos = cursor.fetchall()
                ocupados = []
                for uso in usos:
                    if uso['HoraTreino'] is None or uso['tempo_utilizado_minutos'] is None:
                        continue
                    hora, minuto = map(int, str(uso['HoraTreino']).split(':'))
                    ini = data_dia.replace(hour=hora, minute=minuto, second=0)
                    fim = ini + \
                        timedelta(minutes=uso['tempo_utilizado_minutos'] or 0)
                    ocupados.append((ini, fim))
                # Calcular intervalos ociosos
                atual = inicio_dia
                if not ocupados:
                    # Se não teve uso, ocioso o dia inteiro
                    total_ocioso += (fim_dia -
                                     inicio_dia).total_seconds() // 60
                else:
                    for ini, fim in ocupados:
                        if ini > atual:
                            total_ocioso += (ini - atual).total_seconds() // 60
                        atual = max(atual, fim)
                    if atual < fim_dia:
                        total_ocioso += (fim_dia - atual).total_seconds() // 60
            ociosidade_mensal.append({
                'nome': eq['Nome_Equipamento'],
                'minutos_ocioso': int(total_ocioso),
                'horas_ocioso': round(total_ocioso/60, 2)
            })

    cursor.close()
    conn.close()

    return render_template(
        'relatorio_equipamentos.html',
        unidades=unidades,
        unidade_id=unidade_id,
        unidade_nome=unidade_nome,
        mais_usado=mais_usado,
        menos_usado=menos_usado,
        equipamentos_uso=equipamentos_uso,
        ociosidade=ociosidade_mensal if mes else ociosidade,
        mes=mes
    )
