def test_buscar_paciente_na_tabela_por_id(mock_keycloak, client):
    headers = {
        'Authorization': 'Bearer mocked_token'
    }
    response = client.get('/pacientes/1', headers=headers)
    assert response.status_code == 404
