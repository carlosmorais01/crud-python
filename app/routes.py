from .crud import criarPaciente, listarPacientes, buscarPorId, editarPaciente, deletarPaciente
from flask import current_app

def setup_routes(app):
    with app.app_context():
        tabela = current_app.config.get("TABELA", "pacientes")

    @app.route('/pacientes', methods=['POST'])
    def cadastrarPaciente():
        return criarPaciente(tabela)

    @app.route('/pacientes', methods=['GET'])
    def verPacientes():
        return listarPacientes(tabela)
    
    @app.route('/pacientes/<int:id>', methods=['GET'])
    def verPaciente(id):
        return buscarPorId(id, tabela)
    
    @app.route('/pacientes/<int:id>', methods=['PUT'])
    def editarDados(id):
        return editarPaciente(id, tabela)

    @app.route('/pacientes/<int:id>', methods=['DELETE'])
    def deletarPessoa(id):
        return deletarPaciente(id, tabela)
