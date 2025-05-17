from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/minha-conta')
def minha_conta():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar sua conta.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['usuario']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT Nome_User, Email_user, Data_Nascimento, cpf_user, endereco_user,
               CEP_USER, sexo_user, status_cliente, pagou_mes_atual
        FROM usuario
        WHERE ID_User = %s
    """, (user_id,))
    usuario = cursor.fetchone()
    db.close()
    return render_template('minhaconta.html', usuario=usuario)

@usuarios_bp.route('/gestao-usuarios', methods=['GET', 'POST'])
def gestao_usuarios():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar a gestão de usuários.", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        acao = request.form.get('acao')
        id = request.form.get('id')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        logradouro = request.form.get('logradouro')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        sexo = request.form.get('sexo')
        status = request.form.get('status_cliente')
        pagou = int(request.form.get('pagou_mes_atual') or 0)
        unidade_id = request.form.get('id_unidade')
        plano_id = request.form.get('id_plano')
        data_nascimento = request.form.get('data_nascimento')

        try:
            if acao == 'incluir':
                cursor.execute("""
                    INSERT INTO USUARIO (
                        Nome_User, Email_user, Senha_User, telefone_user,
                        Unidade_Prox_ID, cpf_user, logradouro_user, numero_user,
                        bairro_user, cidade_user, estado_user, CEP_USER,
                        ID_PLANO, sexo_user, status_cliente, pagou_mes_atual, Data_Nascimento
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nome, email, senha, telefone, unidade_id, cpf, logradouro, numero,
                    bairro, cidade, estado, cep, plano_id, sexo, status, pagou, data_nascimento
                ))
                flash("Usuário incluído com sucesso!", "success")

            elif acao == 'editar':
                cursor.execute("""
                    UPDATE USUARIO SET
                        Nome_User=%s,
                        Email_user=%s,
                        telefone_user=%s,
                        logradouro_user=%s,
                        numero_user=%s,
                        bairro_user=%s,
                        cidade_user=%s,
                        estado_user=%s,
                        CEP_USER=%s,
                        sexo_user=%s,
                        status_cliente=%s,
                        pagou_mes_atual=%s,
                        Unidade_Prox_ID=%s,
                        ID_PLANO=%s,
                        Data_Nascimento=%s
                    WHERE ID_User=%s
                """, (
                    nome, email, telefone, logradouro, numero, bairro, cidade, estado, cep,
                    sexo, status, pagou, unidade_id, plano_id, data_nascimento, id
                ))
                flash("Usuário atualizado com sucesso!", "warning")

            elif acao == 'remover':
                cursor.execute("DELETE FROM USUARIO WHERE ID_User = %s", (id,))
                flash("Usuário removido com sucesso!", "error")

            conn.commit()

        except Exception as e:
            conn.rollback()
            flash(f"Erro ao processar operação: {str(e)}", "error")

    cursor.execute("""
        SELECT u.*, un.Nome_Unidade, p.nome_plano
        FROM USUARIO u
        LEFT JOIN UNIDADES un ON u.Unidade_Prox_ID = un.ID_Unidades
        LEFT JOIN PLANO p ON u.ID_PLANO = p.ID_PLANO
    """)
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM UNIDADES")
    unidades = cursor.fetchall()

    cursor.execute("SELECT * FROM PLANO")
    planos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('gestao_usuarios.html', usuarios=usuarios, unidades=unidades, planos=planos) 