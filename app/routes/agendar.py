from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from db import get_db_connection
from datetime import datetime, date, timedelta, time

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

        if not all([id_personal, id_treino, data, hora, id_unidade]):
            flash('Preencha todos os campos para agendar a aula.', 'error')
            return redirect(request.url)

        try:
            data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            flash('Data inválida. Use o seletor de datas.', 'error')
            return redirect(request.url)

        if data_obj < date.today():
            flash('A data deve ser igual ou posterior à data atual.', 'error')
            return redirect(request.url)

        # Converte hora da requisição para datetime.time
        def to_time(h):
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

        hora_nova = to_time(hora)
        inicio_novo = datetime.combine(data_obj, hora_nova)

        # Verificar conflito de horário exato
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_Personal = %s AND DataTreino = %s AND HoraTreino = %s
        """, (id_personal, data_obj, hora_nova))

        if cursor.fetchone():
            flash(
                'Já existe uma aula agendada para esse personal neste dia e horário.', 'error')
            conn.close()
            return redirect(request.url)

        # Verificar conflito considerando duração
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_Personal = %s AND DataTreino = %s
              AND status IN ('Agendado', 'Concluído')
              AND (
                (ADDTIME(HoraTreino, SEC_TO_TIME(DuracaoAula * 60)) > %s AND HoraTreino <= %s)
              )
        """, (id_personal, data_obj, hora_nova, hora_nova))

        if cursor.fetchone():
            flash('Já existe uma aula nesse horário ou sobrepondo outra.', 'error')
            conn.close()
            return redirect(request.url)

        # Verificar se o personal pertence à unidade
        cursor.execute("""
            SELECT 1 FROM personal
            WHERE ID_Personal = %s AND ID_Unidade = %s
        """, (id_personal, id_unidade))

        if not cursor.fetchone():
            flash('O personal selecionado não pertence à unidade escolhida.', 'error')
            conn.close()
            return redirect(request.url)

        # Verificar se o aluno já tem agendamento no mesmo dia e horário
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_usuario = %s AND DataTreino = %s AND HoraTreino = %s
              AND status IN ('Agendado', 'Concluído')
        """, (id_aluno, data_obj, hora_nova))

        if cursor.fetchone():
            flash('Você já possui uma aula agendada nesse dia e horário.', 'error')
            conn.close()
            return redirect(request.url)

        # Buscar duração da aula
        cursor.execute("""
            SELECT COALESCE(SUM(tempo_minutos), 0) as duracao_total
            FROM equipamentos_por_tipo_treino
            WHERE idtipo_de_treino = %s
        """, (id_treino,))
        row_dur = cursor.fetchone()
        duracao_aula = int(
            row_dur['duracao_total']) if row_dur and row_dur['duracao_total'] is not None else 0

        # Verificar sobreposição com outras aulas do aluno
        cursor.execute("""
            SELECT HoraTreino, DuracaoAula FROM agendar_treino
            WHERE ID_usuario = %s AND DataTreino = %s
              AND status IN ('Agendado', 'Concluído')
        """, (id_aluno, data_obj))

        fim_novo = inicio_novo + timedelta(minutes=duracao_aula)
        conflito = False
        for row in cursor.fetchall():
            hora_existente = to_time(row['HoraTreino'])
            inicio_existente = datetime.combine(data_obj, hora_existente)
            duracao_existente = int(
                row['DuracaoAula']) if row['DuracaoAula'] is not None else 0
            fim_existente = inicio_existente + \
                timedelta(minutes=duracao_existente)

            if (inicio_novo < fim_existente and fim_novo > inicio_existente):
                conflito = True
                break

        if conflito:
            flash('Você já possui uma aula agendada que sobrepõe esse horário.', 'error')
            conn.close()
            return redirect(request.url)

        # --- Validação de horário de funcionamento da unidade ---
        # Descobre o dia da semana em português
        dia_semana = data_obj.strftime('%A')
        dia_semana_map = {
            'Monday': 'Segunda',
            'Tuesday': 'Terca',
            'Wednesday': 'Quarta',
            'Thursday': 'Quinta',
            'Friday': 'Sexta',
            'Saturday': 'Sabado',
            'Sunday': 'Domingo'
        }
        dia_em_portugues = dia_semana_map[dia_semana]

        # Busca o horário de funcionamento da unidade para o dia
        cursor.execute("""
            SELECT Hora_Inicio, Hora_Fim FROM horarios_funcionamento
            WHERE FIND_IN_SET(%s, Dias_Semana)
        """, (dia_em_portugues,))
        horario_func = cursor.fetchone()

        if not horario_func:
            flash('A unidade não funciona neste dia da semana.', 'error')
            conn.close()
            return redirect(request.url)

        hora_inicio_func = datetime.strptime(
            str(horario_func['Hora_Inicio']), "%H:%M:%S").time()
        hora_fim_func = datetime.strptime(
            str(horario_func['Hora_Fim']), "%H:%M:%S").time()
        fim_novo = inicio_novo + timedelta(minutes=duracao_aula)
        hora_fim_aula = fim_novo.time()

        hora_inicio_func_dt = datetime.combine(data_obj, hora_inicio_func)
        hora_fim_func_dt = datetime.combine(data_obj, hora_fim_func)
        # Corrige caso o horário de fechamento seja depois da meia-noite (ex: 22:00-01:00)
        if hora_fim_func <= hora_inicio_func:
            hora_fim_func_dt += timedelta(days=1)
        # Validação correta: início e fim da aula dentro do funcionamento
        if not (inicio_novo >= hora_inicio_func_dt and fim_novo <= hora_fim_func_dt):
            flash(
                f'A aula deve começar e terminar dentro do horário de funcionamento da unidade ({hora_inicio_func.strftime("%H:%M")} às {hora_fim_func.strftime("%H:%M")}).', 'error')
            conn.close()
            return redirect(request.url)

        # --- Regra de antecedência por plano ---
        # Buscar o plano do usuário
        cursor.execute(
            "SELECT p.nome_plano FROM usuario u LEFT JOIN plano p ON u.ID_PLANO = p.ID_PLANO WHERE u.ID_User = %s", (id_aluno,))
        row_plano = cursor.fetchone()
        nome_plano = (row_plano['nome_plano'] or '').strip(
        ).lower() if row_plano and row_plano['nome_plano'] else ''
        # Define antecedência mínima por plano
        if nome_plano == 'unlocked':
            antecedencia_min = None  # Sem restrição
        elif nome_plano == 'full':
            antecedencia_min = timedelta(minutes=30)
        elif nome_plano == 'medio' or nome_plano == 'médio':
            antecedencia_min = timedelta(hours=1, minutes=30)
        else:  # basic ou qualquer outro
            antecedencia_min = timedelta(hours=2)
        agora = datetime.now()
        if antecedencia_min is not None and inicio_novo - agora < antecedencia_min:
            if nome_plano == 'medio' or nome_plano == 'médio':
                flash(
                    f'Seu plano exige agendamento com pelo menos {antecedencia_min} de antecedência. Faça upgrade para o plano Full e reserve aulas com ate 30 minutos de antecedencia.', 'error')
            elif nome_plano == 'basic' or nome_plano == 'básico':
                flash(
                    f'Seu plano exige agendamento com pelo menos {antecedencia_min} de antecedência. Faça upgrade para o plano Full e reserve aulas com ate 30 minutos de antecedencia.', 'error')
            else:
                flash(
                    f'Seu plano exige agendamento com pelo menos {antecedencia_min} de antecedência.', 'error')
            conn.close()
            return redirect(request.url)

        try:
            cursor.execute("""
                INSERT INTO agendar_treino
                (ID_usuario, ID_Personal, ID_Tipodetreino, DataTreino, HoraTreino, ID_Unidade_Treino, DuracaoAula, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_aluno, id_personal, id_treino, data_obj, hora_nova, id_unidade, duracao_aula, 'Agendado'))
            conn.commit()
            flash('Aula agendada com sucesso!', 'success')

            # Enviar e-mail de confirmação
            cursor.execute("""
                SELECT u.Email_user, u.Nome_User, p.Nome_Personal, un.Nome_Unidade,
                       CONCAT(un.logradouro_unidade, ', ', un.numero_unidade, ' - ', un.bairro_unidade, ', ', un.cidade_unidade, ' - ', un.estado_unidade, ', CEP: ', un.cep_unidade) AS endereco_unidade
                FROM usuario u
                JOIN personal p ON p.ID_Personal = %s
                JOIN unidades un ON un.ID_Unidades = %s
                WHERE u.ID_User = %s
            """, (id_personal, id_unidade, id_aluno))

            info = cursor.fetchone()

            if info:
                from notifica_aulas import enviar_email

                endereco_formatado = info['endereco_unidade'].replace(' ', '+')

                corpo = f"""
                <html>
                  <body>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; color: #002147; font-family: Arial, sans-serif;">
                      <div style="text-align: left; max-width: 70%;">
                        <h2 style="color: #002147;">Olá {info['Nome_User']},</h2>
                        <p>Sua aula foi agendada com sucesso!</p>

                        <p>
                          <b>Data:</b> {data}<br>
                          <b>Hora:</b> {hora}<br>
                          <b>Personal:</b> {info['Nome_Personal']}<br>
                          <b>Unidade:</b> {info['Nome_Unidade']}<br>
                          <b>Endereço:</b> {info['endereco_unidade']}<br><br>

                          👉 <a href="https://www.google.com/maps/search/?api=1&query={endereco_formatado}" 
                          target="_blank">📍 Ver no Google Maps</a><br><br>

                          Desejamos um ótimo treino! 💪<br><br>
                          Qualquer dúvida, entre em contato com a equipe Fitmax.
                        </p>
                      </div>

                      <div style="text-align: right;">
                        <img src="cid:logo1" alt="Logo Fitmax" width="150">
                      </div>
                    </div>
                  </body>
                </html>
                """

                enviar_email(info['Email_user'],
                             'Confirmação de Agendamento - Fitmax', corpo)

        except Exception as e:
            conn.rollback()
            flash(f'Erro ao agendar aula: {str(e)}', 'error')

    # Carregar dados para o formulário
    cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute(
        "SELECT ID_Personal, Nome_Personal, ID_Unidade FROM personal")
    personais = cursor.fetchall()

    cursor.execute(
        "SELECT idtipo_de_treino, nome_tipo_treino, descricao, ID_Unidade FROM tipo_de_treino")
    treinos = cursor.fetchall()

    conn.close()

    return render_template('agendar.html', personais=personais, treinos=treinos, unidades=unidades)


@agendar_bp.route('/api/horarios_disponiveis', methods=['GET'])
def horarios_disponiveis():
    from datetime import datetime, timedelta, time
    id_unidade = request.args.get('unidade')
    id_personal = request.args.get('personal')
    id_treino = request.args.get('tipo_treino')
    data = request.args.get('data')
    if not all([id_unidade, id_personal, id_treino, data]):
        return jsonify({'horarios': [], 'erro': 'Preencha todos os campos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Buscar duração da aula
        cursor.execute("""
            SELECT COALESCE(SUM(tempo_minutos), 0) as duracao_total
            FROM equipamentos_por_tipo_treino
            WHERE idtipo_de_treino = %s
        """, (id_treino,))
        row_dur = cursor.fetchone()
        duracao_aula = int(
            row_dur['duracao_total']) if row_dur and row_dur['duracao_total'] is not None else 0
        if duracao_aula == 0:
            return jsonify({'horarios': [], 'erro': 'Tipo de treino sem duração configurada.'}), 400

        # Descobre o dia da semana em português
        data_obj = datetime.strptime(data, "%Y-%m-%d").date()
        dia_semana = data_obj.strftime('%A')
        dia_semana_map = {
            'Monday': 'Segunda',
            'Tuesday': 'Terca',
            'Wednesday': 'Quarta',
            'Thursday': 'Quinta',
            'Friday': 'Sexta',
            'Saturday': 'Sabado',
            'Sunday': 'Domingo'
        }
        dia_em_portugues = dia_semana_map[dia_semana]

        # Busca o horário de funcionamento da unidade para o dia
        cursor.execute("""
            SELECT Hora_Inicio, Hora_Fim FROM horarios_funcionamento
            WHERE FIND_IN_SET(%s, Dias_Semana)
        """, (dia_em_portugues,))
        horario_func = cursor.fetchone()
        if not horario_func:
            return jsonify({'horarios': [], 'erro': 'A unidade não funciona neste dia da semana.'}), 200

        def to_time(h):
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
        hora_inicio_func = to_time(horario_func['Hora_Inicio'])
        hora_fim_func = to_time(horario_func['Hora_Fim'])
        hora_inicio_func_dt = datetime.combine(data_obj, hora_inicio_func)
        hora_fim_func_dt = datetime.combine(data_obj, hora_fim_func)
        if hora_fim_func <= hora_inicio_func:
            hora_fim_func_dt += timedelta(days=1)

        # Busca os intervalos de trabalho do personal para o dia
        cursor.execute("""
            SELECT Hora_Inicio, Hora_Fim FROM personal_horario
            WHERE ID_Personal = %s AND Dia_Semana = %s AND Ativo = 1
        """, (id_personal, dia_em_portugues))
        intervalos_trabalho = cursor.fetchall()
        if not intervalos_trabalho:
            return jsonify({'horarios': [], 'erro': 'Este personal não trabalha neste dia.'}), 200

        agora = datetime.now()
        horarios_possiveis = []
        # Para cada intervalo de trabalho do personal, gera horários possíveis na interseção com o funcionamento da unidade
        for intervalo in intervalos_trabalho:
            hora_inicio_p = to_time(intervalo['Hora_Inicio'])
            hora_fim_p = to_time(intervalo['Hora_Fim'])
            inicio_p_dt = datetime.combine(data_obj, hora_inicio_p)
            fim_p_dt = datetime.combine(data_obj, hora_fim_p)
            # Interseção com funcionamento da unidade
            inicio_dt = max(hora_inicio_func_dt, inicio_p_dt)
            fim_dt = min(hora_fim_func_dt, fim_p_dt)
            if fim_dt <= inicio_dt:
                continue  # Não há interseção
            atual = inicio_dt
            while atual + timedelta(minutes=duracao_aula) <= fim_dt:
                # Se for hoje, só mostra horários futuros
                if data_obj > agora.date() or (data_obj == agora.date() and atual.time() >= agora.time()):
                    horarios_possiveis.append(atual.time().strftime('%H:%M'))
                atual += timedelta(minutes=15)

        # Busca agendamentos do personal nesse dia
        cursor.execute("""
            SELECT HoraTreino, DuracaoAula FROM agendar_treino
            WHERE ID_Personal = %s AND DataTreino = %s AND status IN ('Agendado', 'Concluído')
        """, (id_personal, data_obj))
        agendamentos = cursor.fetchall()
        horarios_disponiveis = []
        for h in horarios_possiveis:
            inicio_novo = datetime.combine(
                data_obj, datetime.strptime(h, '%H:%M').time())
            fim_novo = inicio_novo + timedelta(minutes=duracao_aula)
            conflito = False
            for ag in agendamentos:
                hora_existente = ag['HoraTreino']
                if isinstance(hora_existente, timedelta):
                    hora_existente = (datetime.min + hora_existente).time()
                elif isinstance(hora_existente, str):
                    try:
                        hora_existente = datetime.strptime(
                            hora_existente, '%H:%M:%S').time()
                    except ValueError:
                        hora_existente = datetime.strptime(
                            hora_existente, '%H:%M').time()
                elif isinstance(hora_existente, datetime):
                    hora_existente = hora_existente.time()
                inicio_existente = datetime.combine(data_obj, hora_existente)
                duracao_existente = int(
                    ag['DuracaoAula']) if ag['DuracaoAula'] is not None else 0
                fim_existente = inicio_existente + \
                    timedelta(minutes=duracao_existente)
                if (inicio_novo < fim_existente and fim_novo > inicio_existente):
                    conflito = True
                    break
            if not conflito:
                horarios_disponiveis.append(h)
        return jsonify({'horarios': horarios_disponiveis})
    except Exception as e:
        return jsonify({'horarios': [], 'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
