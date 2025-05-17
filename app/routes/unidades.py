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
                    (Nome_Unidade, Endereco_Unidade, Capacidade, Fone, Cidade, Estado, CEP, ID_Regiao)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (nome, endereco, capacidade, fone, cidade, estado, cep, id_regiao))
                flash("Unidade incluída com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE UNIDADES 
                    SET Nome_Unidade=%s, Endereco_Unidade=%s, Capacidade=%s, Fone=%s, Cidade=%s, Estado=%s, CEP=%s, ID_Regiao=%s 
                    WHERE ID_Unidades=%s
                """, (nome, endereco, capacidade, fone, cidade, estado, cep, id_regiao, id))
                flash("Unidade alterada com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM UNIDADES WHERE ID_Unidades=%s", (id,))
                flash("Unidade removida com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("""
        SELECT u.*, r.Nome_Regiao 
        FROM UNIDADES u
        JOIN REGIAO r ON u.ID_Regiao = r.ID_Regiao
    """)
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM REGIAO")
    regioes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('gestao_unidades.html', unidades=unidades, regioes=regioes) 