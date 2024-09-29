from flask import request, jsonify, current_app
from .database import criarConexao

def criarPaciente():
    tabela = current_app.config.get("TABELA", "pacientes")
    data = request.get_json()
    try:
        conn = criarConexao()
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
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Paciente criado"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao criar o paciente: " + str(e)}), 404
    
def listarPacientes(tabela="pacientes"):
    tabela = current_app.config.get("TABELA", "pacientes")
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela}")
        pacientes = cur.fetchall()
        cur.close()
        conn.close()
        if not pacientes:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 403
        return jsonify(pacientes), 200
    
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar os pacientes."}), 405
    
def editarPaciente(id, tabela="pacientes"):
    tabela = current_app.config.get("TABELA", "pacientes")
    data = request.get_json()

    try:
        conn = criarConexao()
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
            conn.commit()
            cur.close()
            conn.close()
        else:
            return jsonify({"mensagem": "Nenhum paciente encontrado com o ID informado"}), 404
        return jsonify({"mensagem": "Paciente atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar o paciente: " + str(e)}), 500
    
def deletarPaciente(id, tabela="pacientes"):
    tabela = current_app.config.get("TABELA", "pacientes")
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {tabela} WHERE id = %s", (id,))
        if cur.rowcount == 0:
            return jsonify({"erro": "Paciente não encontrado"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Paciente deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar o paciente: " + str(e)}), 406
    
def buscarPorId(id, tabela="pacientes"):
    tabela = current_app.config.get("TABELA", "pacientes")
    try:
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id,))
        paciente = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if not paciente:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 404
        return jsonify(paciente), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao paciente usuario: " + str(e)}), 500