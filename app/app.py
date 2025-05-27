from flask import Flask
from routes.auth import auth_bp
from routes.home import home_bp
from routes.usuarios import usuarios_bp
from routes.personais import personais_bp
from routes.equipamentos import equipamentos_bp
from routes.unidades import unidades_bp
from routes.planos import planos_bp
from routes.feedbacks import feedbacks_bp
from routes.treino import treino_bp
from routes.agendar import agendar_bp
from routes.concluir_aula import concluir_bp


app = Flask(__name__)
app.secret_key = 'secreto'

# Registro dos blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(personais_bp)
app.register_blueprint(equipamentos_bp)
app.register_blueprint(unidades_bp)
app.register_blueprint(planos_bp)
app.register_blueprint(feedbacks_bp)
app.register_blueprint(treino_bp)
app.register_blueprint(agendar_bp)
app.register_blueprint(concluir_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
