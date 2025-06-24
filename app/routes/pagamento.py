from flask import Blueprint, render_template, redirect, url_for, flash
from db import get_db_connection  # Use a conexão já existente no projeto
from services.pagamento_service import gerar_cobranca

pagamento_bp = Blueprint('pagamento', __name__)


@pagamento_bp.route('/pagar/<int:user_id>', methods=['GET'])
def pagar(user_id):
    conn = get_db_connection()
    usuario = conn.execute(
        'SELECT * FROM usuario WHERE id = ?', (user_id,)).fetchone()

    if not usuario or not usuario['ID_PLANO']:
        flash("Usuário ou plano não encontrado", "error")
        return redirect(url_for('auth.login'))  # ou para onde fizer sentido

    plano = conn.execute('SELECT * FROM plano WHERE id = ?',
                         (usuario['ID_PLANO'],)).fetchone()
    link_pagamento = gerar_cobranca(usuario, plano)

    return render_template('pagamento.html', usuario=usuario, plano=plano, link=link_pagamento)
