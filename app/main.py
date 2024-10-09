from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .database import criarTabela
from .routes import setup_routes
import os

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CRUD API"
    },
)

def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config['KEYCLOAK_SERVER'] = os.getenv('KEYCLOAK_SERVER', 'http://localhost:8080/auth')
        app.config['KEYCLOAK_REALM'] = os.getenv('KEYCLOAK_REALM', 'meu-reino')
        app.config['KEYCLOAK_CLIENT_ID'] = os.getenv('KEYCLOAK_CLIENT_ID', 'meu-cliente')
        app.config['KEYCLOAK_CLIENT_SECRET'] = os.getenv('KEYCLOAK_CLIENT_SECRET', 'meu-segredo')
        
        app.register_blueprint(swaggerui_blueprint)
        setup_routes(app)
        criarTabela("pacientes")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
