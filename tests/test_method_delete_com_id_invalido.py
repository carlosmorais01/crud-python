def test_deletar_paciente_nao_presente_na_tabela(mock_keycloak, client):
    headers = {
        'Authorization': 'Bearer mocked_token'
    }
    response = client.delete('/pacientes/1', headers=headers)
    assert response.status_code == 404
