def test_obter_pacientes(client):
    response = client.get('/pacientes')
    assert response.status_code == 403
