def test_buscar_paciente_na_tabela_por_id(client):
    response = client.get('/pacientes/1')
    assert response.status_code == 404
