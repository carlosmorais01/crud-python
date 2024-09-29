def test_deletar_paciente_nao_presente_na_tabela(client):
    response = client.delete('/pacientes/1')
    assert response.status_code == 404
