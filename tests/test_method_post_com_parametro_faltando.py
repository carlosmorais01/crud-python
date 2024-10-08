def test_obter_pacientes(client):
    response = client.post('/pacientes', json={
        "nome": "Roberto",
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
        #"nivel_prioridade": 1, || IGNORANDO O NÍVEL DE PRIORIDADE
        "possui_lesao": "true"
    })
    assert response.status_code == 500
