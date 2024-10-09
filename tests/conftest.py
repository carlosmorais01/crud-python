import pytest
from app.main import create_app
from app.database import criarTabela, criarConexao
from unittest.mock import patch

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "TABELA": "teste"
    })
    
    with app.app_context():
        conn = criarConexao()
        cur = conn.cursor()
        criarTabela("teste")
        yield app

        cur.execute("DROP TABLE IF EXISTS teste")
        conn.commit()
        cur.close()
        conn.close()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def mock_keycloak():
    with patch('app.routes.get_keycloak') as mock_get_keycloak:
        mock_instance = mock_get_keycloak.return_value
        mock_instance.introspect.return_value = {
            "active": True
        }
        yield mock_get_keycloak
