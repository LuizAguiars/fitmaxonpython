from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

personais_bp = Blueprint('personais', __name__)


# Ajustando a lógica para aplicar o filtro por unidade corretamente
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
        senha = request.form.get('senha')  # Novo campo senha

        # Converte para int se não vazio, senão None
        id_unidade_db = int(
            id_unidade) if id_unidade and id_unidade.isdigit() else None

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO personal (Nome_Personal, Email_Personal, Especialidade, ID_Unidade, Senha_Personal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome, email, especialidade, id_unidade_db, senha))
                flash("Personal incluído com sucesso!", "success")

            elif acao == 'editar':
                if senha:
                    cursor.execute("""
                        UPDATE personal
                        SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s, Senha_Personal=%s
                        WHERE ID_Personal=%s
                    """, (nome, email, especialidade, id_unidade_db, senha, id))
                else:
                    cursor.execute("""
                        UPDATE personal
                        SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s
                        WHERE ID_Personal=%s
                    """, (nome, email, especialidade, id_unidade_db, id))
                flash("Personal alterado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute(
                    "DELETE FROM personal WHERE id_personal=%s", (id,))
                flash("Personal removido com sucesso!", "error")

            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    unidade_filtro = request.args.get('unidade', '')
    especialidade_filtro = request.args.get('especialidade', '')
    # nome_personal_filtro = request.args.get('nome_personal', '')  # Removido

    # Buscar todos os nomes dos personais para o dropdown
    # cursor.execute(
    #     "SELECT DISTINCT Nome_Personal FROM PERSONAL ORDER BY Nome_Personal"
    # )
    # nomes_personais = cursor.fetchall()

    # Montar a query base
    query = """
        SELECT p.*, u.Nome_Unidade
        FROM PERSONAL p
        LEFT JOIN UNIDADES u ON p.ID_Unidade = u.ID_Unidades
        WHERE 1=1
    """
    params = []

    # if nome_personal_filtro:
    #     query += " AND p.Nome_Personal = %s"
    #     params.append(nome_personal_filtro)

    if unidade_filtro:
        query += " AND u.ID_Unidades = %s"
        params.append(unidade_filtro)

    if especialidade_filtro:
        query += " AND p.Especialidade = %s"
        params.append(especialidade_filtro)

    cursor.execute(query, params)
    personais = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Especialidade FROM PERSONAL")
    especialidades = cursor.fetchall()

    cursor.execute("SELECT id_unidades, nome_unidade FROM unidades")
    unidades_disponiveis = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "gestao_personal.html",
        personais=personais,
        unidades_disponiveis=unidades_disponiveis,
        especialidades=especialidades,
        unidade_filtro=unidade_filtro,
        especialidade_filtro=especialidade_filtro
        # nomes_personais e nome_personal_filtro removidos
    )


@personais_bp.route('/listar-nomes-personais', methods=['GET'])
def listar_nomes_personais():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT nome_personal FROM personal")
    nomes_personais = [row['Nome_Personal'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return render_template('listar_nomes_personais.html', nomes_personais=nomes_personais)
