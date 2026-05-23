import psycopg
from psycopg.types.string import TextLoader
from app.core.config import settings
from app.core.metrics import external_dependency_up, observe_db_operation


def get_connection():
    conn = observe_db_operation("database", "connect", lambda: psycopg.connect(settings.database_url))
    external_dependency_up.labels(dependency="database").set(1)
    # Devolver UUIDs de PostgreSQL como strings directamente
    conn.adapters.register_loader("uuid", TextLoader)
    return conn


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
