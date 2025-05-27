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
        dias_periodo = (datetime.strptime(data_fim, "%Y-%m-%d") - datetime.strptime(data_inicio, "%Y-%m-%d")).days + 1
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
