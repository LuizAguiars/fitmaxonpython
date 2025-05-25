from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

planos_bp = Blueprint('planos', __name__)

@planos_bp.route('/gestao-planos', methods=['GET', 'POST'])
def gestao_planos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de planos.", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        duracao = request.form.get('duracao')
        valor = request.form.get('valor')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO PLANO (nome_plano, descricao, duracao_meses, valor_plano)
                    VALUES (%s, %s, %s, %s)
                """, (nome, descricao, duracao, valor))
                flash("Plano incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE PLANO
                    SET nome_plano=%s, descricao=%s, duracao_meses=%s, valor_plano=%s
                    WHERE ID_PLANO=%s
                """, (nome, descricao, duracao, valor, id))
                flash("Plano alterado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute("DELETE FROM PLANO WHERE ID_PLANO=%s", (id,))
                flash("Plano removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("SELECT * FROM PLANO")
    planos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("gestao_de_planos.html", planos=planos) 