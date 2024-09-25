from flask import request, jsonify
from .database import criarConexao

def criarPaciente():
    data = request.get_json()
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuarios (nome, cpf, data_nascimento, nome_mae, sexo, cartao_sus, 
                                  telefone1, telefone2, email, cep, bairro, logradouro, 
                                  complemento, num_casa, tabagista, etilista, 
                                  nivel_prioridade, possui_lesao) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['nome'], data['cpf'], data['data_nascimento'], data['nome_mae'], data['sexo'], 
              data['cartao_sus'], data['telefone1'], data['telefone2'], data['email'], 
              data['cep'], data['bairro'], data['logradouro'], data['complemento'], 
              data['num_casa'], data['tabagista'], data['etilista'], 
              data['nivel_prioridade'], data['possui_lesao']))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Usuario criado"}), 201
    except Exception as e:
        return jsonify({"erro": "Erro ao criar o usuario: " + str(e)}), 404
    
def listarPacientes():
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios")
        pacientes = cur.fetchall()
        cur.close()
        conn.close()
        if not pacientes:
            return jsonify({"mensagem": "Nenhum usuario encontrado."}), 403
        return jsonify(pacientes), 200
    
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar os usuarios."}), 405
    
def editarPaciente(id):
    data = request.get_json()
    
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("""
            UPDATE usuarios 
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
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Usuario atualizado com sucesso"}), 204
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar o usuario: " + str(e)}), 405
    
def deletarPaciente(id):
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Usuario deletado com sucesso"}), 206
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar o usuario: " + str(e)}), 406
    
def buscarPorId(id):
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        paciente = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not paciente:
            return jsonify({"mensagem": "Nenhum usuario encontrado."}), 407
        return jsonify(paciente), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao procurar usuario: " + str(e)}), 408