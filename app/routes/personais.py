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

    cursor.execute("SELECT ID_Unidades AS ID_Unidades, Nome_Unidade AS Nome_Unidade FROM unidades")
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
