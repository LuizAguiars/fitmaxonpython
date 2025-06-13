from flask import Blueprint, render_template, request
from db import get_db_connection
from datetime import datetime  # Substituir pandas pelo módulo datetime


relatorios_bp = Blueprint('relatorios', __name__)


@relatorios_bp.route('/relatorios/utilizacao_equipamentos', methods=['GET'])
def utilizacao_equipamentos():
    equipamento = request.args.get('equipamento')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    professor = request.args.get('professor')
    unidade = request.args.get('unidade')

    conn = get_db_connection()
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)

    # Consulta de utilização de equipamentos
    query = """
    SELECT ue.id_uso, e.Nome_Equipamento, u.Nome_User, p.Nome_Personal, 
           ag.DataTreino, ag.HoraTreino, un.Nome_Unidade, ue.tempo_utilizado_minutos
    FROM uso_equipamentos ue
    JOIN equipamentos e ON ue.id_equipamento = e.ID_equipamentos
    JOIN usuario u ON ue.id_usuario = u.ID_User
    JOIN agendar_treino ag ON ue.id_treino_agendado = ag.idAgendar_Treino
    JOIN personal p ON ag.ID_Personal = p.ID_Personal
    JOIN unidades un ON ag.ID_Unidade_Treino = un.ID_Unidades
    """

    filtros = []
    params = []

    if equipamento:
        filtros.append("e.Nome_Equipamento LIKE %s")
        params.append(f"%{equipamento}%")
    if data_inicio:
        filtros.append("ag.DataTreino >= %s")
        params.append(data_inicio)
    if data_fim:
        filtros.append("ag.DataTreino <= %s")
        params.append(data_fim)
    if professor:
        filtros.append("p.Nome_Personal LIKE %s")
        params.append(f"%{professor}%")
    if unidade:
        filtros.append("un.Nome_Unidade LIKE %s")
        params.append(f"%{unidade}%")

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    cursor.execute(query, params)
    registros = cursor.fetchall()

    # Dados do relatório resumido
    filtro_sql = " AND ".join(filtros) if filtros else "1=1"

    # Total de clientes cadastrados
    cursor.execute("SELECT COUNT(*) AS total_clientes FROM usuario")
    total_clientes = cursor.fetchone()['total_clientes']

    # Total de clientes ativos no período
    query_ativos = f"""
    SELECT COUNT(DISTINCT ue.id_usuario) AS total_clientes_ativos
    FROM uso_equipamentos ue
    WHERE {filtro_sql}
    """
    cursor.execute(query_ativos, params)
    total_clientes_ativos = cursor.fetchone()['total_clientes_ativos']

    # Tempo total de treino por cliente
    query_tempo_cliente = f"""
    SELECT u.Nome_User AS nome_cliente, SUM(ue.tempo_utilizado_minutos) AS tempo_total
    FROM usuario u
    LEFT JOIN uso_equipamentos ue ON u.ID_User = ue.id_usuario
    WHERE {filtro_sql}
    GROUP BY u.ID_User
    ORDER BY u.Nome_User
    """
    cursor.execute(query_tempo_cliente, params)
    tempo_por_cliente = cursor.fetchall()

    # Soma dos valores dos planos dos clientes ativos
    query_valor_planos = f"""
    SELECT SUM(p.valor_plano) AS soma_planos
    FROM plano p
    JOIN usuario u ON p.ID_Plano = u.ID_Plano
    WHERE u.ID_User IN (
        SELECT DISTINCT ue.id_usuario
        FROM uso_equipamentos ue
        WHERE {filtro_sql}
    )
    """
    cursor.execute(query_valor_planos, params)
    soma_planos = cursor.fetchone()['soma_planos']

    # Tempo usado por equipamentos
    query_tempo_equipamentos = f"""
    SELECT SUM(ue.tempo_utilizado_minutos) AS tempo_usado
    FROM uso_equipamentos ue
    WHERE {filtro_sql}
    """
    cursor.execute(query_tempo_equipamentos, params)
    tempo_usado_equipamentos = cursor.fetchone()['tempo_usado'] or 0

    # Tempo usado por personal trainers (assumindo duração fixa de 60 minutos por treino)
    query_tempo_personal = f"""
    SELECT COUNT(*) * 60 AS tempo_usado
    FROM agendar_treino ag
    WHERE {filtro_sql}
    """
    cursor.execute(query_tempo_personal, params)
    tempo_usado_personal = cursor.fetchone()['tempo_usado'] or 0

    # Cálculo de ociosidade
    if data_inicio and data_fim:
        dias_periodo = (datetime.strptime(data_fim, "%Y-%m-%d") -
                        datetime.strptime(data_inicio, "%Y-%m-%d")).days + 1
    else:
        dias_periodo = 1  # Considerar 1 dia se não houver filtro

    tempo_disponivel_equipamentos = 480 * dias_periodo * total_clientes
    ociosidade_equipamentos = tempo_disponivel_equipamentos - tempo_usado_equipamentos

    tempo_disponivel_personal = 480 * dias_periodo * total_clientes
    ociosidade_personal = tempo_disponivel_personal - tempo_usado_personal

    cursor.close()
    conn.close()

    # Renderizar template com os dados
    return render_template(
        'relatorios.html',
        registros=registros,
        total_clientes=total_clientes,
        total_clientes_ativos=total_clientes_ativos,
        tempo_por_cliente=tempo_por_cliente,
        soma_planos=soma_planos,
        ociosidade_equipamentos=ociosidade_equipamentos,
        ociosidade_personal=ociosidade_personal
    )


@relatorios_bp.route('/relatorios/personal', methods=['GET'])
def relatorio_personal():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Unidades para filtro
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM unidades")
    unidades = cursor.fetchall()
    unidade_id = request.args.get('unidade_id', '')
    mes = request.args.get('mes', '')
    filtro_unidade = ''
    params = []
    if unidade_id:
        filtro_unidade = 'AND ag.ID_Unidade_Treino = %s'
        params.append(unidade_id)
    filtro_mes = ''
    if mes:
        filtro_mes = 'AND DATE_FORMAT(ag.DataTreino, "%Y-%m") = %s'
        params.append(mes)

    # Personal que deu mais/menos aulas
    cursor.execute(f'''
        SELECT p.ID_Personal, p.Nome_Personal, COUNT(ag.idAgendar_Treino) as total_aulas
        FROM personal p
        LEFT JOIN agendar_treino ag ON p.ID_Personal = ag.ID_Personal
        WHERE 1=1 {filtro_unidade} {filtro_mes}
        GROUP BY p.ID_Personal
    ''', params)
    lista_personais = cursor.fetchall()
    mais_personal = max(
        lista_personais, key=lambda x: x['total_aulas'], default=None)
    menos_personal = min(
        lista_personais, key=lambda x: x['total_aulas'], default=None)

    # Tipos de aula mais utilizados
    cursor.execute(f'''
        SELECT t.nome_tipo_treino, COUNT(ag.idAgendar_Treino) as total_aulas, 
               ROUND(SUM(ag.DuracaoAula)/60,2) as total_horas
        FROM tipo_de_treino t
        LEFT JOIN agendar_treino ag ON t.idtipo_de_treino = ag.ID_Tipodetreino
        WHERE 1=1 {filtro_unidade} {filtro_mes}
        GROUP BY t.idtipo_de_treino
        ORDER BY total_aulas DESC
    ''', params)
    tipos_mais_usados = cursor.fetchall()

    # Usuários cadastrados na unidade no mês/ano
    usuarios_unidade = []
    if mes:
        ano, mes_num = mes.split('-')
        cursor.execute(f'''
            SELECT u.ID_Unidades, u.Nome_Unidade, COUNT(us.ID_User) as total_usuarios
            FROM unidades u
            LEFT JOIN usuario us ON us.Unidade_Prox_ID = u.ID_Unidades
                AND YEAR(us.Data_Cadastro_user) = %s AND MONTH(us.Data_Cadastro_user) = %s
            {f'WHERE u.ID_Unidades = %s' if unidade_id else ''}
            GROUP BY u.ID_Unidades
        ''', [ano, mes_num] + ([unidade_id] if unidade_id else []))
        usuarios_unidade = cursor.fetchall()
    else:
        cursor.execute(f'''
            SELECT u.ID_Unidades, u.Nome_Unidade, COUNT(us.ID_User) as total_usuarios
            FROM unidades u
            LEFT JOIN usuario us ON us.Unidade_Prox_ID = u.ID_Unidades
            {f'WHERE u.ID_Unidades = %s' if unidade_id else ''}
            GROUP BY u.ID_Unidades
        ''', [unidade_id] if unidade_id else [])
        usuarios_unidade = cursor.fetchall()

    # Tabela de ociosidade dos personais (ajustado para o dia)
    if unidade_id:
        cursor.execute(
            "SELECT * FROM personal WHERE ID_Unidade = %s", (unidade_id,))
    else:
        cursor.execute("SELECT * FROM personal")
    todos_personais = cursor.fetchall()

    tempo_ocioso_personais = []
    for personal in todos_personais:
        # Tempo disponível diário: soma dos horários cadastrados para o personal
        cursor.execute('''
            SELECT Dia_Semana, Hora_Inicio, Hora_Fim
            FROM personal_horario
            WHERE ID_Personal = %s AND Ativo = 1
        ''', (personal['ID_Personal'],))
        horarios = cursor.fetchall()
        minutos_disponivel_por_semana = 0
        dias_set = set()
        minutos_disponivel_por_dia = {}
        for h in horarios:
            h1 = datetime.strptime(str(h['Hora_Inicio']), "%H:%M:%S")
            h2 = datetime.strptime(str(h['Hora_Fim']), "%H:%M:%S")
            minutos = int((h2 - h1).total_seconds() // 60)
            minutos_disponivel_por_semana += minutos
            dias_set.add(h['Dia_Semana'])
            # Acumula por dia da semana
            if h['Dia_Semana'] not in minutos_disponivel_por_dia:
                minutos_disponivel_por_dia[h['Dia_Semana']] = 0
            minutos_disponivel_por_dia[h['Dia_Semana']] += minutos

        # Dias da semana que o personal trabalha
        dias_com_horario = list(minutos_disponivel_por_dia.keys())

        # --- Determinar o período do relatório ---
        if mes:
            hoje = datetime.now()
            ano, mes_num = mes.split('-')
            ano = int(ano)
            mes_num = int(mes_num)
            if ano == hoje.year and mes_num == hoje.month:
                dia_final = hoje.day
            else:
                from calendar import monthrange
                dia_final = monthrange(ano, mes_num)[1]
            data_inicio_mes = f"{ano}-{mes_num:02d}-01"
            data_fim_mes = f"{ano}-{mes_num:02d}-{dia_final:02d}"
        else:
            hoje = datetime.now()
            ano = hoje.year
            mes_num = hoje.month
            dia_final = hoje.day
            data_inicio_mes = hoje.replace(day=1).strftime("%Y-%m-%d")
            data_fim_mes = hoje.strftime("%Y-%m-%d")

        # --- Calcular dias do mês em que o personal trabalha ---
        import calendar
        dias_trabalho_no_mes = []
        for dia in range(1, dia_final + 1):
            data = datetime(ano, mes_num, dia)
            nome_dia = data.strftime('%A')
            # Traduzir nome do dia para português para bater com o banco
            dias_semana_pt = {
                'Monday': 'Segunda',
                'Tuesday': 'Terca',
                'Wednesday': 'Quarta',
                'Thursday': 'Quinta',
                'Friday': 'Sexta',
                'Saturday': 'Sabado',
                'Sunday': 'Domingo'
            }
            nome_dia_pt = dias_semana_pt[nome_dia]
            if nome_dia_pt in minutos_disponivel_por_dia:
                dias_trabalho_no_mes.append((data.strftime("%Y-%m-%d"), nome_dia_pt))

        # --- Tempo disponível mensal: soma dos minutos disponíveis nos dias que trabalha ---
        minutos_disponivel_mensal = sum(minutos_disponivel_por_dia[dia_semana] for _, dia_semana in dias_trabalho_no_mes)

        # Tempo disponível diário (média por dia com horário)
        minutos_disponivel_diario = 0
        if dias_trabalho_no_mes:
            # Pega o primeiro dia do mês que ele trabalha para mostrar como "diário"
            minutos_disponivel_diario = minutos_disponivel_por_dia[dias_trabalho_no_mes[0][1]]
        else:
            minutos_disponivel_diario = 0

        # --- Tempo utilizado no dia (com filtro de unidade) ---
        # Pega o último dia do filtro (ou hoje)
        if dias_trabalho_no_mes:
            data_dia = dias_trabalho_no_mes[-1][0]
        else:
            data_dia = data_fim_mes

        query_aulas_dia = '''
            SELECT SUM(ag.DuracaoAula) as minutos
            FROM agendar_treino ag
            WHERE ag.ID_Personal = %s AND ag.DataTreino = %s
        '''
        query_params_dia = [personal['ID_Personal'], data_dia]
        if unidade_id:
            query_aulas_dia += ' AND ag.ID_Unidade_Treino = %s'
            query_params_dia.append(unidade_id)
        cursor.execute(query_aulas_dia, query_params_dia)
        minutos_utilizado_dia = cursor.fetchone()['minutos'] or 0

        tempo_ocioso_dia = max(
            0, minutos_disponivel_diario - minutos_utilizado_dia)

        # --- Tempo utilizado no mês (apenas nos dias que trabalha) ---
        minutos_utilizado_mes = 0
        for data_str, _ in dias_trabalho_no_mes:
            query_aulas_mes = '''
                SELECT SUM(ag.DuracaoAula) as minutos
                FROM agendar_treino ag
                WHERE ag.ID_Personal = %s AND ag.DataTreino = %s
            '''
            query_params_mes = [personal['ID_Personal'], data_str]
            if unidade_id:
                query_aulas_mes += ' AND ag.ID_Unidade_Treino = %s'
                query_params_mes.append(unidade_id) 
            cursor.execute(query_aulas_mes, query_params_mes)
            minutos_utilizado_mes += cursor.fetchone()['minutos'] or 0

        query_aulas_mes = '''
            SELECT SUM(ag.DuracaoAula) as minutos
            FROM agendar_treino ag
            WHERE ag.ID_Personal = %s AND ag.DataTreino BETWEEN %s AND %s
        '''
        query_params_mes = [personal['ID_Personal'],
                            data_inicio_mes, data_fim_mes]
        if unidade_id:
            query_aulas_mes += ' AND ag.ID_Unidade_Treino = %s'
            query_params_mes.append(unidade_id)
        cursor.execute(query_aulas_mes, query_params_mes)
        minutos_utilizado_mes = cursor.fetchone()['minutos'] or 0

        tempo_ocioso_mensal = max(
            0, minutos_disponivel_diario * dia_final - minutos_utilizado_mes)

        tempo_ocioso_personais.append({
            "Nome_Personal": personal['Nome_Personal'],
            "tempo_disponivel": minutos_disponivel_diario,
            "tempo_disponivel_horas": f"{minutos_disponivel_diario//60}h {minutos_disponivel_diario % 60}min",
            "tempo_utilizado": minutos_utilizado_dia,
            "tempo_utilizado_horas": f"{minutos_utilizado_dia//60}h {minutos_utilizado_dia % 60}min",
            "tempo_ocioso": tempo_ocioso_dia,
            "tempo_ocioso_horas": f"{tempo_ocioso_dia//60}h {tempo_ocioso_dia % 60}min",
            "tempo_ocioso_mensal": tempo_ocioso_mensal,
            "tempo_ocioso_mensal_horas": f"{tempo_ocioso_mensal//60}h {tempo_ocioso_mensal % 60}min"
        })

    cursor.close()
    conn.close()
    return render_template(
        'relatorio_personal.html',
        unidades=unidades,
        unidade_id=unidade_id,
        mes=mes,
        mais_personal=mais_personal,
        menos_personal=menos_personal,
        lista_personais=lista_personais,
        tipos_mais_usados=tipos_mais_usados,
        usuarios_unidade=usuarios_unidade,
        tempo_ocioso_personais=tempo_ocioso_personais
    )


@relatorios_bp.route('/relatorios/usuarios', methods=['GET'])
def relatorio_usuarios():
    conn = get_db_connection()
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)

    # Consulta peso médio por unidade, pegando o peso da última medição de cada usuário
    cursor.execute('''
        SELECT un.Nome_Unidade, AVG(info.Peso) AS peso_medio
        FROM (
            SELECT ID_User, Peso
            FROM info_usuario iu1
            WHERE DataMedicao = (
                SELECT MAX(DataMedicao)
                FROM info_usuario iu2
                WHERE iu2.ID_User = iu1.ID_User
            )
        ) AS info
        JOIN usuario us ON info.ID_User = us.ID_User
        JOIN unidades un ON us.Unidade_Prox_ID = un.ID_Unidades
        GROUP BY un.Nome_Unidade
    ''')

    pesos_unidade = cursor.fetchall()

    # Novo: consulta para pegar o IMC mais recente de cada usuário
    cursor.execute('''
        SELECT iu1.ID_User, iu1.IMC
        FROM info_usuario iu1
        WHERE iu1.DataMedicao = (
            SELECT MAX(iu2.DataMedicao)
            FROM info_usuario iu2
            WHERE iu2.ID_User = iu1.ID_User
        )
        AND iu1.IMC IS NOT NULL
    ''')
    imc_usuarios = cursor.fetchall()

    # Classificação IMC
    def classificar_imc(imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"

    from collections import Counter
    categorias = [classificar_imc(u['IMC'])
                  for u in imc_usuarios if u['IMC'] is not None]
    contagem = Counter(categorias)
    imc_categorias = [
        {"categoria": cat, "quantidade": contagem.get(cat, 0)}
        for cat in ["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"]
    ]

    cursor.close()
    conn.close()

    return render_template(
        'relatorios_usuarios.html',
        pesos_unidade=pesos_unidade,
        imc_categorias=imc_categorias
    )


@relatorios_bp.route('/relatorios/equipamentos', methods=['GET'])
def relatorio_equipamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar unidades para o filtro
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM unidades")
    unidades = cursor.fetchall()
    print("DEBUG unidades:", unidades)

    unidade_id = request.args.get('unidade_id', '')
    mes = request.args.get('mes', '')

    equipamentos_uso = []
    mais_usado = None
    menos_usado = None
    ociosidade = []

    # Nome da unidade selecionada
    unidade_nome = None
    if unidade_id:
        for u in unidades:
            uid = u.get('ID_Unidades') if 'ID_Unidades' in u else u.get(
                'id_unidades')
            nome = u.get('Nome_Unidade') if 'Nome_Unidade' in u else u.get(
                'nome_unidade')
            if str(uid) == str(unidade_id):
                unidade_nome = nome
                break

    cursor.close()
    conn.close()
    return render_template(
        'relatorio_equipamentos.html',
        unidades=unidades,
        unidade_id=unidade_id,
        unidade_nome=unidade_nome,
        mes=mes,
        equipamentos_uso=equipamentos_uso,
        mais_usado=mais_usado,
        menos_usado=menos_usado,
        ociosidade=ociosidade
    )
