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

    # Obtendo cidades e bairros disponíveis no banco de dados
    cursor.execute("SELECT DISTINCT cidade_unidade FROM UNIDADES WHERE Ativa=1")
    cidades_disponiveis = [row['cidade_unidade'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT bairro_unidade FROM UNIDADES WHERE Ativa=1")
    bairros_disponiveis = [row['bairro_unidade'] for row in cursor.fetchall()]

    # Filtro por cidade e bairro
    cidade_filtro = request.args.get('cidade', '')
    bairro_filtro = request.args.get('bairro', '')

    query = "SELECT u.*, h.Descricao_Horario FROM UNIDADES u LEFT JOIN horarios_funcionamento h ON u.Horario_Funcionamento_ID = h.ID_Horario WHERE Ativa=1"
    params = []

    if cidade_filtro:
        query += " AND cidade_unidade = %s"
        params.append(cidade_filtro)

    if bairro_filtro:
        query += " AND bairro_unidade = %s"
        params.append(bairro_filtro)

    # Paginação
    itens_por_pagina = int(request.args.get('itensPorPagina', 25))
    pagina = int(request.args.get('pagina', 1))
    offset = (pagina - 1) * itens_por_pagina

    query += " LIMIT %s OFFSET %s"
    params.extend([itens_por_pagina, offset])

    cursor.execute(query, params)
    unidades = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM UNIDADES WHERE Ativa=1")
    total_unidades = cursor.fetchone()['total']
    total_paginas = (total_unidades + itens_por_pagina - 1) // itens_por_pagina

    cursor.execute("SELECT * FROM horarios_funcionamento")
    horarios = cursor.fetchall()

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
        bairro_filtro=bairro_filtro
    )
