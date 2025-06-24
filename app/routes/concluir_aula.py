from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

from datetime import datetime, time, timedelta

concluir_bp = Blueprint('concluir', __name__)


@concluir_bp.route('/concluir-aula', methods=['GET', 'POST'])
def concluir_aula():
    if 'usuario' not in session or session.get('tipo') != 'personal':
        flash('Acesso restrito: apenas personais podem concluir aulas.', 'error')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_agenda = request.form.get('id_agenda')
        marcar_ausente = request.form.get('marcar_ausente')
        equipamentos = request.form.getlist('equipamento[]')  # só os marcados
        tempos = request.form.getlist('tempo[]')

        try:
            # Buscar a data e hora da aula agendada
            cursor.execute(
                "SELECT DataTreino, HoraTreino FROM agendar_treino WHERE idAgendar_Treino = %s", (id_agenda,))
            result = cursor.fetchone()
            if not result:
                flash('Aula não encontrada.', 'error')
                return redirect(url_for('concluir.concluir_aula'))
            data_treino = result['DataTreino']
            hora_treino = result['HoraTreino']
            # Combina data e hora para comparar com agora
            try:
                if isinstance(hora_treino, str):
                    hora_treino = datetime.strptime(hora_treino, '%H:%M:%S').time() if len(
                        hora_treino) > 5 else datetime.strptime(hora_treino, '%H:%M').time()
                elif hasattr(hora_treino, 'seconds'):  # timedelta
                    total_seconds = hora_treino.seconds
                    horas = total_seconds // 3600
                    minutos = (total_seconds // 60) % 60
                    hora_treino = time(hour=horas, minute=minutos)
                datahora_treino = datetime.combine(data_treino, hora_treino)
            except Exception:
                flash('Erro: o horário da aula está em formato inválido. Contate o gestor para corrigir o cadastro do treino.', 'error')
                return redirect(url_for('concluir.concluir_aula'))
            agora = datetime.now()

            if marcar_ausente == '1':
                if agora < datahora_treino + timedelta(hours=1):
                    flash(
                        'Só é possível marcar ausência 1 hora após o horário agendado.', 'error')
                    return redirect(url_for('concluir.concluir_aula'))
                cursor.execute(
                    "UPDATE agendar_treino SET status = 'Ausente' WHERE idAgendar_Treino = %s", (id_agenda,))
                conn.commit()
                flash('Aula marcada como ausente.', 'success')
                return redirect(url_for('concluir.concluir_aula'))

            if agora < datahora_treino:
                flash(
                    'Essa aula ainda não pode ser concluída. Só é possível concluir após a data e hora agendada.', 'error')
                return redirect(url_for('concluir.concluir_aula'))

            # Buscar o id_usuario (aluno) da aula agendada
            cursor.execute(
                "SELECT ID_usuario FROM agendar_treino WHERE idAgendar_Treino = %s", (id_agenda,))
            result = cursor.fetchone()
            id_usuario_aluno = result['ID_usuario'] if result else None

            # Só salva os equipamentos marcados (checkbox)
            for equip_id, tempo in zip(equipamentos, tempos):
                cursor.execute("""
                    INSERT INTO uso_equipamentos (id_treino_agendado, id_equipamento, tempo_utilizado_minutos, id_usuario)
                    VALUES (%s, %s, %s, %s)
                """, (id_agenda, equip_id, tempo, id_usuario_aluno))

            cursor.execute("""
                UPDATE agendar_treino SET status = 'Concluído' WHERE idAgendar_Treino = %s
            """, (id_agenda,))

            # Enviar e-mail ao aluno ao concluir aula
            cursor.execute('''
                SELECT u.Email_user, u.Nome_User, a.DataTreino, a.HoraTreino, un.Nome_Unidade,
                       CONCAT(un.logradouro_unidade, ', ', un.numero_unidade, ' - ', un.bairro_unidade, ', ', un.cidade_unidade, ' - ', un.estado_unidade, ', CEP: ', un.cep_unidade) AS endereco_unidade
                FROM usuario u
                JOIN agendar_treino a ON a.ID_usuario = u.ID_User
                JOIN unidades un ON a.ID_Unidade_Treino = un.ID_Unidades
                WHERE a.idAgendar_Treino = %s
            ''', (id_agenda,))
            info = cursor.fetchone()
            if info:
                # Buscar equipamentos usados
                cursor.execute('''
                    SELECT e.Nome_Equipamento, ue.tempo_utilizado_minutos
                    FROM uso_equipamentos ue
                    JOIN equipamentos e ON ue.id_equipamento = e.ID_equipamentos
                    WHERE ue.id_treino_agendado = %s
                ''', (id_agenda,))
                equipamentos_usados = cursor.fetchall()
                equipamentos_html = ''
                if equipamentos_usados:
                    equipamentos_html = '<ul>' + \
                        ''.join(
                            f'<li>{eq["Nome_Equipamento"]} - {eq["tempo_utilizado_minutos"]} min</li>' for eq in equipamentos_usados) + '</ul>'
                else:
                    equipamentos_html = '<i>Nenhum equipamento registrado</i>'
                from notifica_aulas import enviar_email
                endereco_formatado = info['endereco_unidade'].replace(' ', '+')
                corpo = f"""
                <html>
                  <body>
                    <div style='font-family: Arial, sans-serif; color: #002147;'>
                      <h2>Olá {info['Nome_User']},</h2>
                      <p>Sua aula foi concluída na Fitmax!</p>
                      <p>
                        <b>Data:</b> {info['DataTreino']}<br>
                        <b>Hora:</b> {info['HoraTreino']}<br>
                        <b>Unidade:</b> {info['Nome_Unidade']}<br>
                        <b>Endereço:</b> {info['endereco_unidade']}<br><br>
                        <b>Equipamentos utilizados:</b><br>
                        {equipamentos_html}
                        <br>
                        👉 <a href='https://www.google.com/maps/search/?api=1&query={endereco_formatado}' target='_blank'>Ver no Google Maps</a><br><br>
                        <b>Ajude-nos a melhorar:</b> <a href='{url_for('feedbacks.feedbacks', _external=True)}?id_treino={id_agenda}'>Clique aqui para avaliar sua experiência</a>
                      </p>
                      <div style='text-align: right;'><img src='cid:logo1' alt='Logo Fitmax' width='120'></div>
                    </div>
                  </body>
                </html>
                """
                enviar_email(info['Email_user'],
                             'Aula Concluída - Fitmax', corpo)

            conn.commit()
            flash('Aula concluída com sucesso!', 'success')
            # Redireciona para atualizar a lista
            return redirect(url_for('concluir.concluir_aula'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao concluir aula: {str(e)}', 'error')

    hoje = datetime.now().date()

    # Filtros GET
    mes = request.args.get('mes')
    tipo = request.args.get('tipo')
    status = request.args.get('status')

    query = """
        SELECT a.*, t.nome_tipo_treino, u.Nome_User as Nome_Aluno 
        FROM agendar_treino a
        JOIN tipo_de_treino t ON a.ID_Tipodetreino = t.idtipo_de_treino
        JOIN usuario u ON a.ID_usuario = u.ID_User
        WHERE a.ID_Personal = %s AND a.status = 'Agendado'
    """
    params = [session['usuario']]

    if mes:
        query += " AND MONTH(a.DataTreino) = %s"
        params.append(int(mes))
    if tipo:
        query += " AND a.ID_Tipodetreino = %s"
        params.append(int(tipo))

    query += " AND a.DataTreino <= %s"
    params.append(hoje)

    cursor.execute(query, tuple(params))
    aulas = cursor.fetchall()

    # Buscar todos os tipos de treino para o filtro
    cursor.execute(
        "SELECT idtipo_de_treino, nome_tipo_treino FROM tipo_de_treino")
    tipos_treino = cursor.fetchall()

    # Buscar equipamentos de cada tipo de treino
    equipamentos_por_treino = {}
    tipo_ids = set(aula['ID_Tipodetreino'] for aula in aulas)
    for tipo_id in tipo_ids:
        cursor.execute('''
            SELECT e.ID_equipamentos, e.Nome_Equipamento, et.tempo_minutos
            FROM equipamentos_por_tipo_treino et
            JOIN equipamentos e ON et.id_equipamento = e.ID_equipamentos
            WHERE et.idtipo_de_treino = %s
        ''', (tipo_id,))
        equipamentos_por_treino[tipo_id] = cursor.fetchall()

    conn.close()
    return render_template(
        'concluir_aula.html',
        aulas=aulas,
        equipamentos_por_treino=equipamentos_por_treino,
        tipos_treino=tipos_treino
    )
