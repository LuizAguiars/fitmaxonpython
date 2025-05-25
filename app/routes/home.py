from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('inicial.html')

@home_bp.route('/inicial-logado')
def inicial_logado():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('auth.login'))

    nome_completo = session.get('nome', '')
    primeiro_nome = nome_completo.split()[0] if nome_completo else 'Usuário'

    response = make_response(render_template(
        'iniciallogado.html', nome=primeiro_nome))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@home_bp.route('/painel-gestor')
def painel_gestor():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do gestor.", "error")
        return redirect(url_for('auth.login'))
    return render_template('paineldogestor.html')

@home_bp.route('/painel-personal')
def painel_personal():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar o painel do personal.", "error")
        return redirect(url_for('auth.login'))
    return render_template('paineldopersonal.html')

@home_bp.route('/treinos-padrao')
def treinos_padrao():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar os treinos padrão.", "error")
        return redirect(url_for('auth.login'))
    return render_template('treinos_padrao.html') 