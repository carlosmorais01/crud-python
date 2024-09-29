import pytest
from app.main import create_app
from app.database import criarTabela, criarConexao

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
