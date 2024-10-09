def test_obter_pacientes(mock_keycloak, client):
    headers = {
        'Authorization': 'Bearer mocked_token'
    }
    response = client.get('/pacientes', headers=headers)
    assert response.status_code == 404
