import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from db import get_db_connection


# Configurações do Gmail
GMAIL_USER = 'contato.fitmax.cwb@gmail.com'
GMAIL_PASS = 'kgnb uvnl dpcb tfsu'  # Senha de app gerada

# Função para enviar e-mail


def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart('related')
    msg['From'] = GMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    msg_alternative.attach(MIMEText(corpo, 'html'))

    # Anexar a logo
    try:
        with open(r'C:\Users\Luiz Aguiar\Documents\novo teste\fitmaxonpython\app\static\IMG\logo1.png', 'rb') as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header('Content-ID', '<logo1>')
            msg.attach(mime_img)
    except FileNotFoundError:
        print("Logo não encontrada. Verifique o caminho do arquivo logo1.png")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, destinatario, msg.as_string())
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {e}")


# Função principal
def notificar_aulas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    agora = datetime.now()
    daqui_30 = agora + timedelta(minutes=30)

    # Buscar aulas que vão começar em 30 minutos e não foram notificadas
    cursor.execute('''
        SELECT 
            a.idAgendar_Treino, 
            a.DataTreino, 
            a.HoraTreino, 
            a.DuracaoAula, 
            a.status, 
            u.Email_user, 
            u.Nome_User,
            un.Nome_Unidade,
            CONCAT(un.logradouro_unidade, ', ', un.numero_unidade, ' - ', un.bairro_unidade, ', ', un.cidade_unidade, ' - ', un.estado_unidade, ', CEP: ', un.cep_unidade) AS endereco_unidade
        FROM 
            agendar_treino a
        JOIN 
            usuario u ON a.ID_usuario = u.ID_User
        JOIN 
            unidades un ON a.ID_Unidade_Treino = un.ID_Unidades
        WHERE 
            a.status = 'Agendado'
            AND CONCAT(a.DataTreino, ' ', a.HoraTreino) = %s
            AND (a.notificado IS NULL OR a.notificado = 0)
    ''', [daqui_30.strftime('%Y-%m-%d %H:%M:00')])

    aulas = cursor.fetchall()

    for aula in aulas:
        endereco_formatado = aula['endereco_unidade'].replace(' ', '+')

        corpo = f"""
        <html>
          <body>
            <div style="text-align: center;">
              <img src="cid:logo1" alt="Logo Fitmax" width="200"><br><br>

              <h1 style="color: #333;">
                🚨 Sua aula começa às <b>{aula['HoraTreino']}</b> na Fitmax!
              </h1>

              <p style="font-size: 16px;">
                Olá <b>{aula['Nome_User']}</b>,<br><br>
                Este é um lembrete de que você tem uma aula agendada para hoje às 
                <b>{aula['HoraTreino']}</b> na unidade <b>{aula['Nome_Unidade']}</b> da Fitmax.<br><br>

                <b>Unidade:</b> {aula['Nome_Unidade']}<br>
                <b>Endereço:</b> {aula['endereco_unidade']}<br><br>

                👉 <a href="https://www.google.com/maps/search/?api=1&query={endereco_formatado}" target="_blank">
                    📍 Ver no Google Maps
                </a><br><br>

                Desejamos um ótimo treino! 💪<br><br>
                Qualquer dúvida, entre em contato com a equipe Fitmax.
              </p>

              <p style="font-size:12px; color:gray;">
                Este é um e-mail automático. Não responda.
              </p>
            </div>
          </body>
        </html>
        """

        enviar_email(
            aula['Email_user'],
            'Lembrete de Aula - Fitmax',
            corpo
        )

        # Marcar como notificado
        cursor.execute(
            'UPDATE agendar_treino SET notificado = 1 WHERE idAgendar_Treino = %s',
            (aula['idAgendar_Treino'],)
        )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    notificar_aulas()
