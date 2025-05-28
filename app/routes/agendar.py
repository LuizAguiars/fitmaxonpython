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

        # Verificar conflito de horário exato
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_Personal = %s AND DataTreino = %s AND HoraTreino = %s
        """, (id_personal, data_obj, hora))

        if cursor.fetchone():
            flash(
                'Já existe uma aula agendada para esse personal neste dia e horário.', 'error')
            conn.close()
            return redirect(request.url)

        # Verificar conflito considerando duração
        cursor.execute("""
            SELECT 1 FROM agendar_treino
            WHERE ID_Personal = %s
              AND DataTreino = %s
              AND status IN ('Agendado', 'Concluído')
              AND (
                (ADDTIME(HoraTreino, SEC_TO_TIME(DuracaoAula * 60)) > %s AND HoraTreino <= %s)
              )
        """, (id_personal, data_obj, hora, hora))

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

        # Buscar duração da aula
        cursor.execute("""
            SELECT COALESCE(SUM(tempo_minutos), 0) as duracao_total
            FROM equipamentos_por_tipo_treino
            WHERE idtipo_de_treino = %s
        """, (id_treino,))
        row = cursor.fetchone()
        duracao_aula = row['duracao_total'] if row else 0

        try:
            # Inserir agendamento
            cursor.execute("""
                INSERT INTO agendar_treino
                (ID_usuario, ID_Personal, ID_Tipodetreino, DataTreino, HoraTreino, ID_Unidade_Treino, DuracaoAula, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_aluno, id_personal, id_treino, data, hora, id_unidade, duracao_aula, 'Agendado'))
            conn.commit()
            flash('Aula agendada com sucesso!', 'success')

            # Enviar e-mail de confirmação
            cursor.execute("""
                SELECT u.Email_user, u.Nome_User, p.Nome_Personal, un.Nome_Unidade,
                       CONCAT(un.Endereco_Unidade, ', ', un.Cidade, ' - ', un.Estado, ', CEP: ', un.CEP) AS endereco_unidade
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
                        <p style="color: #002147;">Sua aula foi agendada com sucesso!</p>

                        <p style="color: #002147;">
                          <b>Data:</b> {data}<br>
                          <b>Hora:</b> {hora}<br>
                          <b>Personal:</b> {info['Nome_Personal']}<br>
                          <b>Unidade:</b> {info['Nome_Unidade']}<br>
                          <b>Endereço:</b> {info['endereco_unidade']}<br><br>

                          👉 <a href="https://www.google.com/maps/search/?api=1&query={endereco_formatado}" 
                          target="_blank" style="color: #002147; text-decoration: underline;">
                          📍 Ver no Google Maps
                          </a><br><br>

                          Desejamos um ótimo treino! 💪<br><br>
                          <span style="color: #002147;">Qualquer dúvida, entre em contato com a equipe Fitmax.</span>
                        </p>
                      </div>

                      <div style="text-align: right;">
                        <img src="cid:logo1" alt="Logo Fitmax" width="150">
                      </div>
                    </div>
                  </body>
                </html>
                """

                enviar_email(
                    info['Email_user'],
                    'Confirmação de Agendamento - Fitmax',
                    corpo
                )
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

    return render_template(
        'agendar.html',
        personais=personais,
        treinos=treinos,
        unidades=unidades
    )
