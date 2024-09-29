from app.database import criarConexao
def test_editar_paciente(client, app):
    with app.app_context():
        conn = criarConexao()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO teste (nome, cpf, data_nascimento, nome_mae, sexo, cartao_sus, 
            telefone1, telefone2, email, cep, bairro, logradouro, complemento, num_casa, 
            tabagista, etilista, nivel_prioridade, possui_lesao) VALUES ('Teste', '123.456.789-11', 
            '1989-10-12', 'Teste', 'M', '123456789101112', '65113251312', '67123141213', 'teste@teste.com', '12345-654', 
            'Céu Azul', 'Rua do Sol', 'Apto. 12', '123', 'true', 'false', '2', 'true')
        """)
        conn.commit()
        cur.close()
        conn.close()
    response = client.put('/pacientes/1', json={
        "nome": "Carlos",
        "cpf": "123.456.789-10",
        "data_nascimento": "2001-03-17",
        "nome_mae": "Maria",
        "sexo": "M",
        "cartao_sus": 123456789101213,
        "telefone1": 62997234123,
        "telefone2": 62994415231,
        "email": "teste@gmail.com",
        "cep": "73453-654",
        "bairro": "Avenida 1",
        "logradouro": "Rua 2",
        "complemento": "Comercial Airton",
        "num_casa": 423,
        "tabagista": "true",
        "etilista": "false",
        "nivel_prioridade": 1,
        "possui_lesao": "true"
    })
    assert response.status_code == 200
