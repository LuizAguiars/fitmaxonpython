from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection


treino_bp = Blueprint('treino', __name__)


@treino_bp.route('/treinos', methods=['GET', 'POST'])
def gerenciar_treinos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
        else:
            nome = request.form.get('nome')
            descricao = request.form.get('descricao')
            equipamentos = request.form.getlist('equipamentos[]')
            tempos = request.form.getlist('tempos[]')

            print("DEBUG - nome:", nome)
            print("DEBUG - descricao:", descricao)
            print("DEBUG - equipamentos:", equipamentos)
            print("DEBUG - tempos:", tempos)

            # Validação extra para evitar valores nulos
            if not nome or not equipamentos or not tempos or any(e == '' for e in equipamentos) or any(t == '' for t in tempos):
                flash(
                    'Preencha todos os campos obrigatórios do treino e equipamentos.', 'error')
                conn.close()
                return redirect(request.url)

            try:
                cursor.execute(
                    "INSERT INTO tipo_de_treino (nome_tipo_treino, descricao) VALUES (%s, %s)", (nome, descricao))
                id_treino = cursor.lastrowid
                print("DEBUG - id_treino inserido:", id_treino)

                for equip_id, tempo in zip(equipamentos, tempos):
                    print("DEBUG - Inserindo equipamento:",
                          equip_id, "tempo:", tempo)
                    cursor.execute("""
                        INSERT INTO equipamentos_por_tipo_treino (idtipo_de_treino, id_equipamento, tempo_minutos)
                        VALUES (%s, %s, %s)
                    """, (int(id_treino), int(equip_id), int(tempo)))

                conn.commit()
                print("DEBUG - Commit realizado")
                flash('Treino criado com sucesso!', 'success')
            except Exception as e:
                import traceback
                print("DEBUG - Erro ao criar treino:", str(e))
                traceback.print_exc()
                conn.rollback()
                flash(f'Erro ao criar treino: {str(e)}', 'error')

    # Buscar todos os treinos
    cursor.execute("SELECT * FROM tipo_de_treino")
    treinos_raw = cursor.fetchall()

    # Buscar todos os equipamentos por treino (ajuste nos nomes das colunas)
    cursor.execute("""
        SELECT et.idtipo_de_treino, GROUP_CONCAT(e.Nome_Equipamento SEPARATOR ', ') AS equipamentos
        FROM equipamentos_por_tipo_treino et
        JOIN equipamentos e ON et.id_equipamento = e.ID_equipamentos
        GROUP BY et.idtipo_de_treino
    """)
    equipamentos_por_treino = {
        row['idtipo_de_treino']: row['equipamentos'] for row in cursor.fetchall()}

    # Renomear campos para manter compatibilidade com o template
    treinos = []
    for t in treinos_raw:
        treinos.append({
            'ID_Tipo_Treino': t['idtipo_de_treino'],
            'Nome_Treino': t['nome_tipo_treino'],
            'Descricao': t['descricao'],
            'equipamentos': equipamentos_por_treino.get(t['idtipo_de_treino'], '')
        })

    cursor.execute("SELECT * FROM equipamentos")
    equipamentos = cursor.fetchall()

    conn.close()
    return render_template('gestao_treinos.html', treinos=treinos, equipamentos=equipamentos)
