from .crud import criarPaciente, listarPacientes, buscarPorId, editarPaciente, deletarPaciente
from flask import request, jsonify, current_app
from keycloak import KeycloakOpenID
from functools import wraps

def setup_routes(app):
    # Configurando Keycloak dentro do setup_routes
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
    
    # Instância do Keycloak
    keycloak_openid = get_keycloak()

    # Middleware para verificar o token
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]  # Token Bearer

            if not token:
                return jsonify({"message": "Token não informado"}), 401

            try:
                # Valida o token com o Keycloak
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
    
    @app.route('/pacientes/<int:id>', methods=['GET'])
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
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        keycloak_openid = get_keycloak()
        token = keycloak_openid.token(username, password)
    
        return jsonify(token)
