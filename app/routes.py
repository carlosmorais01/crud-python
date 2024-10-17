from .crud import criarPaciente, listarPacientes, buscarPorId, editarPaciente, deletarPaciente
from flask import request, jsonify, current_app
from keycloak import KeycloakOpenID
from functools import wraps
from keycloak.exceptions import KeycloakAuthenticationError

def get_keycloak():
    server_url = current_app.config.get("KEYCLOAK_SERVER")
    realm_name = current_app.config.get("KEYCLOAK_REALM")
    client_id = current_app.config.get("KEYCLOAK_CLIENT_ID")
    client_secret = current_app.config.get("KEYCLOAK_CLIENT_SECRET")

    return KeycloakOpenID(
        server_url=server_url,
        realm_name=realm_name,
        client_id=client_id,
        client_secret_key=client_secret
    )

def setup_routes(app):
    keycloak_openid = get_keycloak()

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({"message": "Token não informado"}), 401

            try:
                keycloak_openid.introspect(token)
            except Exception as e:
                return jsonify({"message": f"Token inválido ou expirado: {str(e)}"}), 401

            return f(*args, **kwargs)
        
        return decorated

    @app.route('/pacientes', methods=['POST'])
    @token_required
    def cadastrarPaciente():
        return criarPaciente()

    @app.route('/pacientes', methods=['GET'])
    @token_required
    def verPacientes():
        return listarPacientes()
    
    @app.route('/pacientes/<id>', methods=['GET'])
    @token_required
    def verPaciente(id):
        return buscarPorId(id)
    
    @app.route('/pacientes/<int:id>', methods=['PUT'])
    @token_required
    def editarDados(id):
        return editarPaciente(id)

    @app.route('/pacientes/<int:id>', methods=['DELETE'])
    @token_required
    def deletarPessoa(id):
        return deletarPaciente(id)
        
    @app.route('/auth', methods=['POST'])
    def authenticate():
        try:
            data = request.json
            if not data:
                return jsonify({"mensagem": "Dados de autenticação ausentes."}), 400

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"mensagem": "Username e password são obrigatórios."}), 400

            keycloak_openid = get_keycloak()

            token = keycloak_openid.token(username, password)
            return jsonify(token), 200
        
        except KeycloakAuthenticationError:
            return jsonify({"mensagem": "Credenciais inválidas."}), 401

        except Exception as e:
            return jsonify({"mensagem": f"Erro interno: {str(e)}"}), 500
