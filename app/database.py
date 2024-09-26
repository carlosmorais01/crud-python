import psycopg2
import os

def criarConexao():
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB", "postgres"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "acs"),
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5432")
    )
    return conn

def criarTabela():
    conn = criarConexao()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cpf CHAR(14) UNIQUE NOT NULL,
            data_nascimento DATE NOT NULL,
            nome_mae VARCHAR(255) NOT NULL,
            sexo VARCHAR(5) NOT NULL,
            cartao_sus CHAR(15) NOT NULL,
            telefone1 VARCHAR(20) NOT NULL,
            telefone2 VARCHAR(20),
            email VARCHAR(255),
            cep VARCHAR(10),
            bairro VARCHAR(255),
            logradouro VARCHAR(255),
            complemento VARCHAR(255),
            num_casa VARCHAR(10),
            tabagista BOOLEAN DEFAULT FALSE,
            etilista BOOLEAN DEFAULT FALSE,
            possui_lesao BOOLEAN DEFAULT FALSE,
            nivel_prioridade INTEGER CHECK (nivel_prioridade BETWEEN 1 AND 3)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()