import pytest
from app import create_app

@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.sqlite3"
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-key",
        "DATABASE": str(db_path),
        "MAX_SAMPLE_LENGTH": 1000,
        "MAX_CONTENT_LENGTH": 65536,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
