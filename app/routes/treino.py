from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection


treino_bp = Blueprint('treino', __name__)


@treino_bp.route('/treinos', methods=['GET', 'POST'])
def gerenciar_treinos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obter unidade selecionada via POST ou GET
    unidade_selecionada = request.values.get('unidade')

    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'remover':
            treino_id = request.form.get('id')
            if treino_id:
                try:
                    cursor.execute(
                        "DELETE FROM tipo_de_treino WHERE idtipo_de_treino = %s", (treino_id,))
                    conn.commit()
                    flash('Treino removido com sucesso!', 'success')
                except Exception as e:
                    conn.rollback()
                    flash(f'Erro ao remover treino: {str(e)}', 'error')
            else:
                flash('ID do treino não informado para remoção.', 'error')
        elif acao == 'incluir':
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            id_unidade = request.form.get('unidade')
            equipamentos = request.form.getlist('equipamentos[]')
            tempos = request.form.getlist('tempos[]')
            unidade_selecionada = id_unidade  # manter seleção após submit

            # Validação extra para evitar valores nulos
            if not nome or not equipamentos or not tempos or any(e == '' for e in equipamentos) or any(t == '' for t in tempos) or not id_unidade:
                flash(
                    'Preencha todos os campos obrigatórios do treino, equipamentos e unidade.', 'error')
                conn.close()
                return redirect(request.url)

            # NOVO: Validar se todos os equipamentos pertencem à unidade selecionada
            cursor.execute(
                "SELECT ID_equipamentos FROM equipamentos WHERE ID_unidade_equipamento = %s", (id_unidade,))
            equipamentos_validos = {
                str(row['ID_equipamentos']) for row in cursor.fetchall()}
            if not all(e in equipamentos_validos for e in equipamentos):
                flash(
                    'Só é permitido selecionar equipamentos da unidade escolhida.', 'error')
                conn.close()
                return redirect(request.url)

            try:
                cursor.execute(
                    "INSERT INTO tipo_de_treino (nome_tipo_treino, descricao, ID_Unidade) VALUES (%s, %s, %s)", (nome, descricao, id_unidade))
                id_treino = cursor.lastrowid

                for equip_id, tempo in zip(equipamentos, tempos):
                    cursor.execute("""
                        INSERT INTO equipamentos_por_tipo_treino (idtipo_de_treino, id_equipamento, tempo_minutos)
                        VALUES (%s, %s, %s)
                    """, (int(id_treino), int(equip_id), int(tempo)))

                conn.commit()
                flash('Treino criado com sucesso!', 'success')
            except Exception as e:
                import traceback
                traceback.print_exc()
                conn.rollback()
                flash(f'Erro ao criar treino: {str(e)}', 'error')

    # Buscar todas as unidades para o dropdown
    cursor.execute("SELECT id_unidades, nome_unidade FROM unidades")
    unidades = cursor.fetchall()

    # Buscar todos os treinos (sem filtro)
    cursor.execute("SELECT * FROM tipo_de_treino")
    treinos_raw = cursor.fetchall()

    cursor.execute("""
        SELECT et.idtipo_de_treino, GROUP_CONCAT(e.Nome_Equipamento SEPARATOR ', ') AS equipamentos
        FROM equipamentos_por_tipo_treino et
        JOIN equipamentos e ON et.id_equipamento = e.ID_equipamentos
        GROUP BY et.idtipo_de_treino
    """)
    equipamentos_por_treino = {
        row['idtipo_de_treino']: row['equipamentos'] for row in cursor.fetchall()}

    treinos = []
    for t in treinos_raw:
        treinos.append({
            'ID_Tipo_Treino': t['idtipo_de_treino'],
            'Nome_Treino': t['nome_tipo_treino'],
            'Descricao': t['descricao'],
            'equipamentos': equipamentos_por_treino.get(t['idtipo_de_treino'], ''),
            'ID_Unidade': t.get('ID_Unidade')
        })

    cursor.execute("SELECT * FROM equipamentos")
    equipamentos = cursor.fetchall()

    conn.close()
    return render_template(
        'gestao_treinos.html',
        treinos=treinos,
        equipamentos=equipamentos,
        unidades=unidades,
        unidade_selecionada=unidade_selecionada
    )
