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
                    INSERT INTO EQUIPAMENTOS
                    (Nome_Equipamento, descricao_equipamentos, data_de_compra,
                     ID_unidade_equipamento, id_status_do_equipamento, idtipo_equipamento)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo))
                flash("Equipamento incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE EQUIPAMENTOS
                    SET Nome_Equipamento=%s, descricao_equipamentos=%s, data_de_compra=%s,
                        ID_unidade_equipamento=%s, id_status_do_equipamento=%s, idtipo_equipamento=%s
                    WHERE ID_equipamentos=%s
                """, (nome, descricao, data_compra, id_unidade, id_status, id_tipo, id))
                flash("Equipamento atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM EQUIPAMENTOS WHERE ID_equipamentos = %s", (id,))
                flash("Equipamento removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("""
        SELECT e.*, u.Nome_Unidade, s.status_do_Equipamento, t.nome_tipo_equipamento
        FROM EQUIPAMENTOS e
        LEFT JOIN UNIDADES u ON e.ID_unidade_equipamento = u.ID_Unidades
        LEFT JOIN status_dos_Equipamentos s ON e.id_status_do_equipamento = s.idstatus_dos_Equipamentos
        LEFT JOIN tipo_equipamento t ON e.idtipo_equipamento = t.idtipo_equipamento
    """)
    equipamentos = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM status_dos_Equipamentos")
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
        tipos_equipamento=tipos_equipamento
    ) 