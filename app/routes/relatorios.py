from flask import Blueprint, render_template
from db import get_db_connection

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/utilizacao_equipamentos', methods=['GET'])
def utilizacao_equipamentos():
    conn = get_db_connection()
    if conn is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = conn.cursor(dictionary=True)

    try:
        # Query 1: Total clients and active clients
        cursor.execute("SELECT COUNT(*) AS total_clientes FROM usuario")
        total_clientes = cursor.fetchone()['total_clientes']

        cursor.execute("SELECT COUNT(*) AS clientes_ativos FROM usuario WHERE status_cliente = 'ativo'")
        clientes_ativos = cursor.fetchone()['clientes_ativos']

        # Query 2: Sum of membership values
        cursor.execute("SELECT SUM(valor_plano) AS soma_matriculas FROM plano")
        soma_matriculas = cursor.fetchone()['soma_matriculas']

        # Query 3: Total equipment usage time
        cursor.execute("SELECT SUM(tempo_utilizado_minutos) AS tempo_total_uso_equip FROM uso_equipamentos")
        tempo_total_uso_equip = cursor.fetchone()['tempo_total_uso_equip']

        # Query 4: Total training time for personal trainers
        cursor.execute("""
            SELECT SUM(ue.tempo_utilizado_minutos) AS tempo_total_treino_personal
            FROM uso_equipamentos ue
            JOIN agendar_treino ag ON ue.id_treino_agendado = ag.idAgendar_Treino
        """)
        tempo_total_treino_personal = cursor.fetchone()['tempo_total_treino_personal']

        # Passa os resultados como registros para o template
        registros = [
            {"descricao": "Total de clientes", "valor": total_clientes},
            {"descricao": "Clientes ativos", "valor": clientes_ativos},
            {"descricao": "Soma das matrículas", "valor": soma_matriculas},
            {"descricao": "Tempo total de uso dos equipamentos", "valor": tempo_total_uso_equip},
            {"descricao": "Tempo total de treino dos personal trainers", "valor": tempo_total_treino_personal},
        ]

    except Exception as e:
        registros = [{"descricao": "Erro", "valor": str(e)}]

    finally:
        cursor.close()
        conn.close()

    return render_template('relatorios.html', registros=registros)
