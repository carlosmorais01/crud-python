from app.database import criarConexao
def test_deletar_paciente_presente_na_tabela(mock_keycloak, client, app):
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
    headers = {
        'Authorization': 'Bearer mocked_token'
    }
    response = client.delete('/pacientes/1', headers=headers)
    assert response.status_code == 200
