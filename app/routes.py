from .crud import criarPaciente, listarPacientes, buscarPorId, editarPaciente, deletarPaciente

def setup_routes(app):

    @app.route('/pacientes', methods=['POST'])
    def cadastrarPaciente():
        return criarPaciente()

    @app.route('/pacientes', methods=['GET'])
    def verPacientes():
        return listarPacientes()
    
    @app.route('/pacientes/<int:id>', methods=['GET'])
    def verPaciente(id):
        return buscarPorId(id)
    
    @app.route('/pacientes/<int:id>', methods=['PUT'])
    def editarDados(id):
        return editarPaciente(id)

    @app.route('/pacientes/<int:id>', methods=['DELETE'])
    def deletarPessoa(id):
        return deletarPaciente(id)
