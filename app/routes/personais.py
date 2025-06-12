from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
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
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        genero = request.form.get('genero')
        bio = request.form.get('bio')
        certificado_nome = request.form.get('certificado_nome')
        certificado_codigo = request.form.get('certificado_codigo')
        certificado_emissor = request.form.get('certificado_emissor')
        certificado_data = request.form.get('certificado_data')

        # Converte para int se não vazio, senão None
        id_unidade_db = int(
            id_unidade) if id_unidade and id_unidade.isdigit() else None

        # Validação de idade mínima (20 anos) apenas para data de nascimento
        from datetime import datetime, date

        def idade_completa(data_nasc):
            if not data_nasc:
                return 0
            try:
                nasc = datetime.strptime(data_nasc, '%Y-%m-%d').date()
            except Exception:
                return 0
            hoje = date.today()
            idade = hoje.year - nasc.year - \
                ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            return idade
        # Só valida se o campo for data de nascimento
        if data_nascimento:
            if idade_completa(data_nascimento) < 20:
                flash('Personal deve ter pelo menos 20 anos completos.', 'error')
                return redirect(url_for('personais.gestao_personal'))

        # Validação opcional de formato para certificado_data (não obrigatória)
        if certificado_data:
            try:
                datetime.strptime(certificado_data, '%Y-%m-%d')
            except ValueError:
                flash('Data do certificado inválida.', 'error')
                return redirect(url_for('personais.gestao_personal'))

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO personal (Nome_Personal, Email_Personal, Especialidade, ID_Unidade, Senha_Personal, DataNascimento, Telefone, CPF, Genero, Bio, CertificadoNome, CertificadoCodigo, CertificadoEmissor, CertificadoData)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, email, especialidade, id_unidade_db, senha, data_nascimento, telefone, cpf, genero, bio, certificado_nome, certificado_codigo, certificado_emissor, certificado_data))
                flash("Personal incluído com sucesso!", "success")

            elif acao == 'editar':
                if senha:
                    cursor.execute("""
                        UPDATE personal
                        SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s, Senha_Personal=%s, DataNascimento=%s, Telefone=%s, CPF=%s, Genero=%s, Bio=%s, CertificadoNome=%s, CertificadoCodigo=%s, CertificadoEmissor=%s, CertificadoData=%s
                        WHERE ID_Personal=%s
                    """, (nome, email, especialidade, id_unidade_db, senha, data_nascimento, telefone, cpf, genero, bio, certificado_nome, certificado_codigo, certificado_emissor, certificado_data, id))
                else:
                    cursor.execute("""
                        UPDATE personal
                        SET Nome_Personal=%s, Email_Personal=%s, Especialidade=%s, ID_Unidade=%s, DataNascimento=%s, Telefone=%s, CPF=%s, Genero=%s, Bio=%s, CertificadoNome=%s, CertificadoCodigo=%s, CertificadoEmissor=%s, CertificadoData=%s
                        WHERE ID_Personal=%s
                    """, (nome, email, especialidade, id_unidade_db, data_nascimento, telefone, cpf, genero, bio, certificado_nome, certificado_codigo, certificado_emissor, certificado_data, id))
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

    # Montar a query base
    query = """
        SELECT p.*, u.Nome_Unidade
        FROM PERSONAL p
        LEFT JOIN UNIDADES u ON p.ID_Unidade = u.ID_Unidades
        WHERE 1=1
    """
    params = []

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

    cursor.execute(
        "SELECT ID_Unidades AS ID_Unidades, Nome_Unidade AS Nome_Unidade FROM unidades")
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


@personais_bp.route('/horario-personal', methods=['POST'])
def horario_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de personais.", "error")
        return redirect(url_for('personais.gestao_personal'))

    id_unidade = request.form.get('unidade')
    id_personal = request.form.get('personal')
    from collections import defaultdict
    dias_semana = ['Segunda', 'Terca', 'Quarta',
                   'Quinta', 'Sexta', 'Sabado', 'Domingo']
    # Monta dict: horarios[dia] = [ {inicio, fim, ativo}, ... ]
    horarios_dict = defaultdict(list)
    for dia in dias_semana:
        idx = 0
        while True:
            inicio = request.form.get(f'horarios[{dia}][{idx}][inicio]')
            fim = request.form.get(f'horarios[{dia}][{idx}][fim]')
            if inicio is None and fim is None:
                break
            # Salva se ambos preenchidos
            if inicio and fim:
                horarios_dict[dia].append({'inicio': inicio, 'fim': fim})
            idx += 1

    if not id_unidade or not id_personal:
        flash('Selecione unidade e personal.', 'error')
        return redirect(url_for('personais.gestao_personal'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    from datetime import datetime, time, timedelta

    def to_time(h):
        if not h:
            return None
        if isinstance(h, time):
            return h
        elif isinstance(h, timedelta):
            return (datetime.min + h).time()
        elif isinstance(h, datetime):
            return h.time()
        elif isinstance(h, str):
            h = h.strip()
            try:
                return datetime.strptime(h, "%H:%M:%S").time()
            except ValueError:
                return datetime.strptime(h, "%H:%M").time()
        raise TypeError("Hora inválida")
    try:
        erros = []
        inseridos = 0
        for dia, intervalos in horarios_dict.items():
            if not intervalos:
                continue
            # Buscar horário de funcionamento da unidade para o dia
            cursor.execute("""
                SELECT Hora_Inicio, Hora_Fim FROM horarios_funcionamento
                WHERE FIND_IN_SET(%s, Dias_Semana)
            """, (dia,))
            horario_func = cursor.fetchone()
            if not horario_func:
                erros.append(f'{dia}: Unidade não funciona nesse dia.')
                continue
            hora_inicio_func = to_time(horario_func['Hora_Inicio'])
            hora_fim_func = to_time(horario_func['Hora_Fim'])
            # Remove todos os horários antigos do personal para o dia
            cursor.execute(
                "DELETE FROM personal_horario WHERE ID_Personal=%s AND Dia_Semana=%s", (id_personal, dia))
            for info in intervalos:
                hora_inicio = to_time(info['inicio'])
                hora_fim = to_time(info['fim'])
                if not hora_inicio or not hora_fim or hora_inicio < hora_inicio_func or hora_fim > hora_fim_func or hora_fim <= hora_inicio:
                    erros.append(
                        f'{dia}: Horário {info["inicio"]}-{info["fim"]} inválido ou fora do funcionamento da unidade.')
                    continue
                cursor.execute("""
                    INSERT INTO personal_horario (ID_Personal, Dia_Semana, Hora_Inicio, Hora_Fim)
                    VALUES (%s, %s, %s, %s)
                """, (id_personal, dia, hora_inicio, hora_fim))
                inseridos += 1
        conn.commit()
        if inseridos:
            flash(f'{inseridos} horário(s) cadastrado(s) com sucesso!', 'success')
        if erros:
            flash('Ocorreram erros em alguns dias: ' + '; '.join(erros), 'error')
    except Exception as e:
        conn.rollback()
        flash(f'Erro ao cadastrar horários: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('personais.gestao_personal'))


@personais_bp.route('/api/horarios-personal')
def api_horarios_personal():
    if 'usuario' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    id_personal = request.args.get('personal')
    if not id_personal:
        return jsonify({'horarios': []})
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Dia_Semana, DATE_FORMAT(Hora_Inicio, '%H:%i') as hora_inicio, DATE_FORMAT(Hora_Fim, '%H:%i') as hora_fim
        FROM personal_horario
        WHERE ID_Personal=%s
    """, (id_personal,))
    horarios = [
        {'dia_semana': row['Dia_Semana'],
            'hora_inicio': row['hora_inicio'], 'hora_fim': row['hora_fim']}
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return jsonify({'horarios': horarios})


@personais_bp.route('/salvar-modelo-horario', methods=['POST'])
def salvar_modelo_horario():
    if 'usuario' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    data = request.get_json()
    nome_modelo = data.get('nome_modelo')
    id_unidade = data.get('id_unidade')
    horarios = data.get('horarios')  # dict: {dia: [{inicio, fim}, ...], ...}
    if not nome_modelo or not id_unidade or not horarios:
        return jsonify({'erro': 'Dados incompletos'}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO modelo_horario (Nome, ID_Unidade)
            VALUES (%s, %s)
        """, (nome_modelo, id_unidade))
        id_modelo = cursor.lastrowid
        for dia, intervalos in horarios.items():
            for intervalo in intervalos:
                cursor.execute("""
                    INSERT INTO modelo_horario_intervalo (ID_Modelo, Dia_Semana, Hora_Inicio, Hora_Fim)
                    VALUES (%s, %s, %s, %s)
                """, (id_modelo, dia, intervalo['inicio'], intervalo['fim']))
        conn.commit()
        return jsonify({'ok': True, 'id_modelo': id_modelo})
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@personais_bp.route('/listar-modelos-horario', methods=['GET'])
def listar_modelos_horario():
    if 'usuario' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    id_unidade = request.args.get('id_unidade')
    if id_unidade is not None and id_unidade != '':
        try:
            id_unidade_int = int(id_unidade)
        except Exception:
            id_unidade_int = None
    else:
        id_unidade_int = None
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Modelos globais (ID_Unidade IS NULL) ou da unidade
        if id_unidade_int is not None:
            cursor.execute("""
                SELECT ID_Modelo, Nome, ID_Unidade
                FROM modelo_horario
                WHERE ID_Unidade = %s OR ID_Unidade IS NULL
                ORDER BY Nome
            """, (id_unidade_int,))
        else:
            cursor.execute("""
                SELECT ID_Modelo, Nome, ID_Unidade
                FROM modelo_horario
                WHERE ID_Unidade IS NULL
                ORDER BY Nome
            """)
        modelos = cursor.fetchall()
        return jsonify({'modelos': modelos})
    finally:
        cursor.close()
        conn.close()


@personais_bp.route('/modelo-horario/<int:id_modelo>', methods=['GET'])
def get_modelo_horario(id_modelo):
    if 'usuario' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT Dia_Semana, Hora_Inicio, Hora_Fim
            FROM modelo_horario_intervalo
            WHERE ID_Modelo = %s
            ORDER BY FIELD(Dia_Semana, 'Segunda','Terca','Quarta','Quinta','Sexta','Sabado','Domingo'), Hora_Inicio
        """, (id_modelo,))
        intervalos = cursor.fetchall()
        # Organiza por dia
        horarios = {}
        for row in intervalos:
            dia = row['Dia_Semana']
            if dia not in horarios:
                horarios[dia] = []
            horarios[dia].append({'inicio': str(row['Hora_Inicio'])[
                                 :5], 'fim': str(row['Hora_Fim'])[:5]})
        return jsonify({'horarios': horarios})
    finally:
        cursor.close()
        conn.close()
