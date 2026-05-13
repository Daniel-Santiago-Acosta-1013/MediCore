import os

# Establecer variables de entorno ANTES de importar la app
os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", "postgresql://medicore:secret@db:5432/medicore")
os.environ["SECRET_KEY"] = "test-secret-key"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_connection


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_conn():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
