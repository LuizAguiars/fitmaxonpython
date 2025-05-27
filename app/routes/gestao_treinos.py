from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection
from datetime import datetime, date

agendar_bp = Blueprint('agendar', __name__)


@agendar_bp.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if 'usuario' not in session or session.get('tipo') != 'aluno':
        flash('Faça login como aluno para agendar uma aula.', 'error')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_personal = request.form.get('personal')
        id_treino = request.form.get('tipo_treino')
        data = request.form.get('data')
        hora = request.form.get('hora')
        id_unidade = request.form.get('unidade')
        id_aluno = session['usuario']

        # Verificar se todos os campos estão preenchidos
        if not all([id_personal, id_treino, data, hora, id_unidade]):
            flash('Preencha todos os campos para agendar a aula.', 'error')
            return redirect(request.url)

        # Validação da data
        try:
            data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            flash('Data inválida. Use o seletor de datas.', 'error')
            return redirect(request.url)

        if data_obj < date.today():
            flash('A data deve ser igual ou posterior à data atual.', 'error')
            return redirect(request.url)

        # Verificar conflito de horário
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_Personal = %s AND DataTreino = %s AND HoraTreino = %s
        """, (id_personal, data_obj, hora))

        if cursor.fetchone():
            flash(
                'Já existe uma aula agendada para esse personal neste dia e horário.', 'error')
            conn.close()
            return redirect(request.url)

        # Validação de integridade referencial: personal deve pertencer à unidade
        cursor.execute(
            "SELECT 1 FROM personal WHERE ID_Personal = %s AND ID_Unidade = %s", (id_personal, id_unidade))
        if not cursor.fetchone():
            flash('O personal selecionado não pertence à unidade escolhida.', 'error')
            conn.close()
            return redirect(request.url)

        try:
            cursor.execute("""
                INSERT INTO agendar_treino (ID_usuario, ID_Personal, ID_Tipodetreino, DataTreino, HoraTreino, ID_Unidade_Treino, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_aluno, id_personal, id_treino, data, hora, id_unidade, 'Agendado'))
            conn.commit()
            flash('Aula agendada com sucesso!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao agendar aula: {str(e)}', 'error')

    # Listar dados para o formulário
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM UNIDADES")
    unidades = cursor.fetchall()

    # Buscar todos personais com sua unidade
    cursor.execute(
        "SELECT ID_Personal, Nome_Personal, ID_Unidade FROM personal")
    personais = cursor.fetchall()

    # Buscar todos tipos de treino (sem unidade)
    cursor.execute(
        "SELECT idtipo_de_treino, nome_tipo_treino, descricao FROM tipo_de_treino")
    treinos = cursor.fetchall()

    conn.close()
    return render_template('agendar.html', personais=personais, treinos=treinos, unidades=unidades)


@agendar_bp.route('/gestao_treinos', methods=['GET', 'POST'])
def gestao_treinos():
    if 'usuario' not in session or session.get('tipo') != 'gestor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST' and request.form.get('acao') == 'incluir':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        id_unidade = request.form.get('unidade')

        # Validações
        if not all([nome, id_unidade]):
            flash('Preencha todos os campos obrigatórios.', 'error')
        else:
            try:
                cursor.execute(
                    "INSERT INTO tipo_de_treino (nome_tipo_treino, descricao, ID_Unidade) VALUES (%s, %s, %s)",
                    (nome, descricao, id_unidade)
                )
                conn.commit()
                flash('Treino cadastrado com sucesso!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'Erro ao cadastrar treino: {str(e)}', 'error')

    # Buscar treinos cadastrados
    cursor.execute("""
        SELECT tt.idtipo_de_treino, tt.nome_tipo_treino, tt.descricao, u.Nome_Unidade
        FROM tipo_de_treino tt
        JOIN UNIDADES u ON tt.ID_Unidade = u.ID_Unidades
    """)
    treinos = cursor.fetchall()

    # Buscar unidades
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM UNIDADES")
    unidades = cursor.fetchall()

    conn.close()
    return render_template('gestao_treinos.html', treinos=treinos, unidades=unidades)
