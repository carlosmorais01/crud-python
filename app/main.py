from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from app.database import criarTabela
from app.routes import setup_routes
import os

SWAGGER_URL = '/api/docs'
API_URL = '\static\swagger.yml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CRUD API"
    },
)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(swaggerui_blueprint)
    setup_routes(app)
    criarTabela()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
