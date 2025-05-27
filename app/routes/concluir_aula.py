from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

from datetime import datetime, time

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
                # Se já for time, segue normalmente
                datahora_treino = datetime.combine(data_treino, hora_treino)
            except Exception:
                flash('Erro: o horário da aula está em formato inválido. Contate o gestor para corrigir o cadastro do treino.', 'error')
                return redirect(url_for('concluir.concluir_aula'))
            agora = datetime.now()
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

            conn.commit()
            flash('Aula concluída com sucesso!', 'success')
            # Redireciona para atualizar a lista
            return redirect(url_for('concluir.concluir_aula'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao concluir aula: {str(e)}', 'error')

    hoje = datetime.now().date()
    cursor.execute("""
        SELECT a.*, t.nome_tipo_treino, u.Nome_User as Nome_Aluno 
        FROM agendar_treino a
        JOIN tipo_de_treino t ON a.ID_Tipodetreino = t.idtipo_de_treino
        JOIN usuario u ON a.ID_usuario = u.ID_User
        WHERE a.ID_Personal = %s AND a.status = 'Agendado' AND a.DataTreino <= %s
    """, (session['usuario'], hoje))

    aulas = cursor.fetchall()

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
    return render_template('concluir_aula.html', aulas=aulas, equipamentos_por_treino=equipamentos_por_treino)
