from flask import request, jsonify
from .database import criarConexao

_conn = None

def get_db_connection():
    global _conn
    if _conn is None:
        _conn = criarConexao()
    return _conn

def execute_db_operation(operation):
    try:
        conn = get_db_connection()
        result = operation(conn)
        conn.commit()
        return result
    except Exception as e:
        return jsonify({"erro": f"Erro ao realizar operação no banco de dados: {str(e)}"}), 500
    finally:
        conn.close()
        global _conn
        _conn = None

def criarPaciente(tabela):
    data = request.get_json()

    def insertPaciente(conn):
        cur = conn.cursor()
        cur.execute(f"""
            INSERT INTO {tabela} (nome, cpf, data_nascimento, nome_mae, sexo, cartao_sus, 
            telefone1, telefone2, email, cep, bairro, logradouro,complemento, num_casa, 
            tabagista, etilista, nivel_prioridade, possui_lesao) VALUES (%s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['nome'], data['cpf'], data['data_nascimento'], data['nome_mae'], data['sexo'], 
                data['cartao_sus'], data['telefone1'], data['telefone2'], data['email'], 
                data['cep'], data['bairro'], data['logradouro'], data['complemento'], 
                data['num_casa'], data['tabagista'], data['etilista'], 
                data['nivel_prioridade'], data['possui_lesao']))
        cur.close()
        return jsonify({"mensagem": "Paciente criado"}), 200
    
    return execute_db_operation(insertPaciente)
    
def listarPacientes(tabela):
    def getPacientes(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela}")
        pacientes = cur.fetchall()
        cur.close()
        
        if not pacientes:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 404
        return jsonify(pacientes), 200
    
    return execute_db_operation(getPacientes)
    
def editarPaciente(id, tabela):
    data = request.get_json()

    def putPaciente(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id,))
        paciente = cur.fetchone()

        if paciente:
            cur.execute(f"""
                UPDATE {tabela} 
                SET nome = %s, cpf = %s, data_nascimento = %s, nome_mae = %s, sexo = %s, 
                    cartao_sus = %s, telefone1 = %s, telefone2 = %s, email = %s, cep = %s, 
                    bairro = %s, logradouro = %s, complemento = %s, num_casa = %s, 
                    tabagista = %s, etilista = %s, nivel_prioridade = %s, possui_lesao = %s
                WHERE id = %s
                """, (data['nome'], data['cpf'], data['data_nascimento'], data['nome_mae'], data['sexo'], 
                data['cartao_sus'], data['telefone1'], data.get('telefone2'), data['email'], 
                data['cep'], data['bairro'], data['logradouro'], 
                data.get('complemento'), data['num_casa'], 
                data['tabagista'], data['etilista'], 
                data['nivel_prioridade'], data['possui_lesao'], id))
            cur.close()
        else:
            return jsonify({"mensagem": "Nenhum paciente encontrado com o ID informado"}), 404
        
        return jsonify({"mensagem": "Paciente atualizado com sucesso"}), 200
    
    return execute_db_operation(putPaciente)
    
def deletarPaciente(id, tabela):
    def deletePaciente(conn):
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {tabela} WHERE id = %s", (id,))
        if cur.rowcount == 0:
            return jsonify({"erro": "Paciente não encontrado"}), 404

        cur.close()
        return jsonify({"mensagem": "Paciente deletado com sucesso"}), 200
    
    return execute_db_operation(deletePaciente)
    
def buscarPorId(id, tabela):
    def get_by_id(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id,))
        paciente = cur.fetchone()
        cur.close()
        if not paciente:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 404
        
        return jsonify(paciente), 200
    
    return execute_db_operation(get_by_id)