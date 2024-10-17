from flask import request, jsonify, current_app
from .database import get_db_connection
from psycopg2 import IntegrityError

campos = [
    "id", "nome", "cpf", "data_nascimento", "nome_mae", "sexo", "cartao_sus",
    "telefone1", "telefone2", "email", "cep", "bairro", "logradouro",
    "complemento", "num_casa", "tabagista", "etilista", "nivel_prioridade",
    "possui_lesao"
]

def execute_db_operation(operation):
    try:
        conn = get_db_connection()
        result = operation(conn)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Erro ao realizar operação no banco de dados: {str(e)}"}), 500

def criarPaciente():
    tabela = current_app.config.get("TABELA", "pacientes")
    data = request.get_json()

    def insertPaciente(conn):
        try:
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO {tabela} ({", ".join(campos[1:])}) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (data['nome'], data['cpf'], data['data_nascimento'], data['nome_mae'], 
                  data['sexo'], data['cartao_sus'], data['telefone1'], data['telefone2'], 
                  data['email'], data['cep'], data['bairro'], data['logradouro'], 
                  data['complemento'], data['num_casa'], data['tabagista'], 
                  data['etilista'], data['nivel_prioridade'], data['possui_lesao']))

            paciente_id = cur.fetchone()[0]
            conn.commit()
            cur.close()

            response_data = {campo: data[campo] for campo in campos[1:]}
            response_data["id"] = paciente_id

            return jsonify(response_data), 201

        except IntegrityError as e:
            conn.rollback()
            return jsonify({
                "error": "Campos únicos informados já pertencem a algum outro paciente cadastrado",
                "details": str(e)
            }), 409

    return execute_db_operation(insertPaciente)

def listarPacientes():
    tabela = current_app.config.get("TABELA", "pacientes")

    def fetchPacientes(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela} ORDER BY nome ASC")
        rows = cur.fetchall()
        cur.close()

        if not rows:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 404

        pacientes = [dict(zip(campos, row)) for row in rows]
        return jsonify(pacientes), 200

    return execute_db_operation(fetchPacientes)

def editarPaciente(id):
    tabela = current_app.config.get("TABELA", "pacientes")
    data = request.get_json()

    def putPaciente(conn):
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id,))
        paciente = cur.fetchone()
        if paciente:
            try:
                cur.execute(f"""
                    UPDATE {tabela} SET {", ".join([f"{campo} = %s" for campo in campos[1:]])}
                    WHERE id = %s
                """, (*[data[campo] for campo in campos[1:]], id))
                cur.close()
            except IntegrityError as e:
                conn.rollback()
                return jsonify({
                    "error": "Campos únicos informados já pertencem a algum outro paciente cadastrado",
                    "details": str(e)
                }), 409
        else:
            return jsonify({"mensagem": "Nenhum paciente encontrado com o ID informado"}), 404
        return jsonify({"mensagem": "Paciente atualizado com sucesso"}), 200
    
    return execute_db_operation(putPaciente)

def deletarPaciente(id):
    tabela = current_app.config.get("TABELA", "pacientes")

    def deletePaciente(conn):
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {tabela} WHERE id = %s", (id,))
        if cur.rowcount == 0:
            return jsonify({"erro": "Paciente não encontrado"}), 404

        cur.close()
        return jsonify({"mensagem": "Paciente deletado com sucesso"}), 200
    
    return execute_db_operation(deletePaciente)

def buscarPorId(id):
    tabela = current_app.config.get("TABELA", "pacientes")

    try:
        id = int(id)  
        if id < 1: 
            raise ValueError("O ID deve ser um número inteiro positivo.")
    except (ValueError, TypeError):
        return jsonify({"mensagem": "ID inválido. Deve ser um número inteiro positivo."}), 400

    def get_by_id(conn):
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabela} WHERE id = %s", (id,))
        paciente = cur.fetchone()
        cur.close()

        if not paciente:
            return jsonify({"mensagem": "Nenhum paciente encontrado."}), 404

        paciente_dict = dict(zip(campos, paciente))
        return jsonify(paciente_dict), 200
    
    return execute_db_operation(get_by_id)
