FROM python:3.12-slim

# =============================================================================
# Instalar uv de forma estática
# =============================================================================
COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /usr/local/bin/uv

WORKDIR /app

# =============================================================================
# Dependencias del sistema (compilación, Sqitch, PostgreSQL client)
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    sqitch \
    libdbd-pg-perl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Copiar manifestos primero para cachear capa de dependencias
# =============================================================================
COPY pyproject.toml .
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY db/ ./db/

# Instalar dependencias del proyecto de forma precisa con uv
RUN uv pip install --system -e .

# Permisos para scripts
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000

# =============================================================================
# Entrypoint: espera DB, corre Sqitch, levanta API
# =============================================================================
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
