from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

personais_bp = Blueprint('personais', __name__)

@personais_bp.route('/gestao-personal', methods=['GET', 'POST'])
def gestao_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de personais.", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        especialidade = request.form.get('especialidade')
        id_unidade = request.form.get('id_unidade')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO PERSONAL (Nome_Personal, Email_Personal, Especialidade, ID_Unidade)
                    VALUES (%s, %s, %s, %s)
                """, (nome, email, especialidade, id_unidade))
                flash("Personal incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE PERSONAL
                    SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s
                    WHERE ID_Personal=%s
                """, (nome, email, especialidade, id_unidade, id))
                flash("Personal alterado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM PERSONAL WHERE ID_Personal=%s", (id,))
                flash("Personal removido com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("""
        SELECT p.*, u.Nome_Unidade
        FROM PERSONAL p
        LEFT JOIN UNIDADES u ON p.ID_Unidade = u.ID_Unidades
    """)
    personais = cursor.fetchall()

    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("gestao_personal.html", personais=personais, unidades=unidades) 