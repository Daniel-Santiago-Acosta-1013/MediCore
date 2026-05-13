import psycopg
from psycopg.types.string import TextLoader
from app.core.config import settings


def get_connection():
    conn = psycopg.connect(settings.database_url)
    # Devolver UUIDs de PostgreSQL como strings directamente
    conn.adapters.register_loader("uuid", TextLoader)
    return conn


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
