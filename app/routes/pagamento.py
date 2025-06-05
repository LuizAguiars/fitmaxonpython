from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Usuario, Plano
from services.pagamento_service import gerar_cobranca

pagamento_bp = Blueprint('pagamento', __name__)


@pagamento_bp.route('/pagar/<int:user_id>', methods=['GET'])
def pagar(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario or not usuario.ID_PLANO:
        flash("Usuário ou plano não encontrado", "error")
        return redirect(url_for('auth.login'))  # ou para onde fizer sentido

    plano = Plano.query.get(usuario.ID_PLANO)
    link_pagamento = gerar_cobranca(usuario, plano)

    return render_template('pagamento.html', usuario=usuario, plano=plano, link=link_pagamento)
