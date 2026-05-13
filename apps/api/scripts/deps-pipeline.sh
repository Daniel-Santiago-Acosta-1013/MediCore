#!/bin/bash
set -euo pipefail

# =============================================================================
# Pipeline local de dependencias para MediCore API
# =============================================================================
# Script standalone alternativo a 'task deps:pipeline'.
# Ideal para CI/CD o entornos donde Task no está instalado.
#
# Uso:
#   ./scripts/deps-pipeline.sh
# =============================================================================

echo "=========================================="
echo "📦 MediCore API - Dependency Pipeline"
echo "=========================================="

# Verificar que uv esté instalado
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' no está instalado. Instálalo desde https://github.com/astral-sh/uv"
    exit 1
fi

# -----------------------------------------------------------------------------
# 1. Lock
# -----------------------------------------------------------------------------
echo ""
echo "🔒 [1/4] Generando/actualizando uv.lock..."
uv lock

# -----------------------------------------------------------------------------
# 2. Sync
# -----------------------------------------------------------------------------
echo ""
echo "📦 [2/4] Sincronizando entorno virtual con uv.lock..."
uv sync

# -----------------------------------------------------------------------------
# 3. Audit
# -----------------------------------------------------------------------------
echo ""
echo "🔍 [3/4] Auditando vulnerabilidades con pip-audit..."

if uv run pip-audit --desc; then
    echo "✅ Auditoría completada sin vulnerabilidades críticas."
else
    echo "⚠️  Se encontraron vulnerabilidades. Revisa el reporte arriba."
    # No salimos con error para permitir ver todo el pipeline
fi

# -----------------------------------------------------------------------------
# 4. Outdated
# -----------------------------------------------------------------------------
echo ""
echo "📋 [4/4] Chequeando paquetes desactualizados..."
uv pip list --outdated || true

echo ""
echo "=========================================="
echo "✅ Pipeline de dependencias completado"
echo "=========================================="
