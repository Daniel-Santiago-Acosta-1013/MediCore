#!/bin/bash
set -euo pipefail

# =============================================================================
# Entrypoint para el contenedor de MediCore API
# =============================================================================
# Este script se ejecuta al iniciar el contenedor. Realiza:
# 1. Espera activa a que PostgreSQL esté disponible
# 2. Aplicación automática de migraciones con Sqitch
# 3. Inicio de la aplicación FastAPI con Uvicorn
# =============================================================================

POSTGRES_HOST="${POSTGRES_HOST:-db}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_USER="${POSTGRES_USER:-medicore}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-secret}"
POSTGRES_DB="${POSTGRES_DB:-medicore}"

echo "=========================================="
echo "🚀 MediCore API - Entrypoint"
echo "=========================================="

# -----------------------------------------------------------------------------
# 1. Esperar a PostgreSQL
# -----------------------------------------------------------------------------
echo "⏳ Esperando PostgreSQL en ${POSTGRES_HOST}:${POSTGRES_PORT}..."

RETRIES=30
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
  RETRIES=$((RETRIES - 1))
  if [ $RETRIES -le 0 ]; then
    echo "❌ PostgreSQL no está disponible después de 30 intentos. Abortando."
    exit 1
  fi
  echo "   ... intento $((30 - RETRIES))/30"
  sleep 1
done

echo "✅ PostgreSQL está listo."

# -----------------------------------------------------------------------------
# 2. Aplicar migraciones con Sqitch
# -----------------------------------------------------------------------------
echo "📦 Aplicando migraciones de Sqitch..."

cd /app/db

DB_URI="db:pg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

if sqitch deploy "$DB_URI"; then
  echo "✅ Migraciones aplicadas correctamente."
else
  echo "⚠️  Sqitch deploy falló. Verifica el estado de la base de datos."
  echo "   Intentando mostrar estado..."
  sqitch status "$DB_URI" || true
  # No abortamos para permitir debugging manual, pero en producción
  # podrías hacer 'exit 1' aquí.
fi

# -----------------------------------------------------------------------------
# 3. Iniciar aplicación
# -----------------------------------------------------------------------------
cd /app

echo "=========================================="
echo "🌐 Iniciando Uvicorn..."
echo "   URL: http://0.0.0.0:8000"
echo "   Docs: http://0.0.0.0:8000/docs"
echo "=========================================="

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
