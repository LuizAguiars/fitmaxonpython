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
                    (Nome_Unidade, Capacidade, Fone, logradouro_unidade, numero_unidade, bairro_unidade, cidade_unidade, estado_unidade, cep_unidade, CNPJ, Email, Horario_Funcionamento_ID, Ativa)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
                """, (
                    nome,
                    capacidade,
                    fone,
                    request.form.get('logradouro'),
                    request.form.get('numero'),
                    request.form.get('bairro'),
                    request.form.get('cidade'),
                    request.form.get('estado'),
                    request.form.get('cep'),
                    request.form.get('cnpj'),
                    request.form.get('email'),
                    request.form.get('horario_funcionamento_id')
                ))
                flash("Unidade incluída com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE UNIDADES 
                    SET Nome_Unidade=%s, Capacidade=%s, Fone=%s, logradouro_unidade=%s, numero_unidade=%s, bairro_unidade=%s, cidade_unidade=%s, estado_unidade=%s, cep_unidade=%s, CNPJ=%s, Email=%s, Horario_Funcionamento_ID=%s
                    WHERE ID_Unidades=%s
                """, (
                    nome,
                    capacidade,
                    fone,
                    request.form.get('logradouro'),
                    request.form.get('numero'),
                    request.form.get('bairro'),
                    request.form.get('cidade'),
                    request.form.get('estado'),
                    request.form.get('cep'),
                    request.form.get('cnpj'),
                    request.form.get('email'),
                    request.form.get('horario_funcionamento_id'),
                    id
                ))
                flash("Unidade alterada com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "UPDATE UNIDADES SET Ativa=0 WHERE ID_Unidades=%s", (id,))
                flash("Unidade desativada com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    # Filtro de itens por página
    itens_por_pagina = int(request.args.get('itensPorPagina', 25))
    pagina = int(request.args.get('pagina', 1))
    offset = (pagina - 1) * itens_por_pagina

    cursor.execute("""
        SELECT COUNT(*) as total FROM UNIDADES
    """)
    total_unidades = cursor.fetchone()['total']
    total_paginas = (total_unidades + itens_por_pagina - 1) // itens_por_pagina

    cursor.execute("""
        SELECT u.*, h.Descricao_Horario 
        FROM UNIDADES u
        LEFT JOIN horarios_funcionamento h ON u.Horario_Funcionamento_ID = h.ID_Horario
        LIMIT %s OFFSET %s
    """, (itens_por_pagina, offset))
    unidades = cursor.fetchall()

    # Não busca mais regioes
    horarios = []
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
        itens_por_pagina=itens_por_pagina
    )
