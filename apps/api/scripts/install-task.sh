#!/bin/bash
set -euo pipefail

# =============================================================================
# Instala Task (taskfile runner) LOCALMENTE en el proyecto
# Metodo oficial: https://taskfile.dev/installation/
# =============================================================================
# Esto descarga el binario de Task a ./bin/task dentro del proyecto.
# No requiere privilegios de administrador ni afecta el sistema global.
# Ademas, configura automaticamente el PATH para que 'task' funcione
# desde cualquier lugar dentro del proyecto.
#
# Uso:
#   ./scripts/install-task.sh
#   task up
# =============================================================================

INSTALL_DIR="./bin"
TASK_BIN="$INSTALL_DIR/task"

echo "=========================================="
echo "🔧 Instalando Task localmente..."
echo "=========================================="

# Crear directorio bin si no existe
mkdir -p "$INSTALL_DIR"

# Descargar e instalar usando el script oficial de Task
# -d = debug/output visible
# -b = directorio destino
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b "$INSTALL_DIR"

echo ""
echo "=========================================="
echo "✅ Task instalado localmente"
echo "=========================================="
echo ""
echo "Ruta: $TASK_BIN"
echo "Version: $($TASK_BIN --version)"
echo ""

# =============================================================================
# Configurar PATH automaticamente
# =============================================================================
configure_path() {
  local shell_rc=""
  local path_entry='export PATH="./bin:$PATH"'

  if [ -n "${ZSH_VERSION:-}" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
    shell_rc="$HOME/.zshrc"
  elif [ -n "${BASH_VERSION:-}" ] || [ "$(basename "$SHELL")" = "bash" ]; then
    shell_rc="$HOME/.bashrc"
  elif [ "$(basename "$SHELL")" = "fish" ]; then
    shell_rc="$HOME/.config/fish/config.fish"
    path_entry='set -gx PATH ./bin $PATH'
  fi

  if [ -n "$shell_rc" ] && [ -f "$shell_rc" ]; then
    if grep -qF './bin:$PATH' "$shell_rc" 2>/dev/null || grep -qF './bin $PATH' "$shell_rc" 2>/dev/null; then
      echo "ℹ️  El PATH ya esta configurado en $shell_rc"
    else
      echo "" >> "$shell_rc"
      echo "# MediCore API - Task local" >> "$shell_rc"
      echo "$path_entry" >> "$shell_rc"
      echo "✅ PATH configurado automaticamente en $shell_rc"
    fi
  else
    echo "⚠️  No se pudo detectar el archivo de configuracion del shell."
    echo "   Agrega manualmente esta linea a tu ~/.bashrc o ~/.zshrc:"
    echo "   export PATH=\"./bin:\$PATH\""
  fi
}

configure_path

echo ""
echo "=========================================="
echo "🚀 Listo para usar"
echo "=========================================="
echo ""
echo "Ejecuta en una nueva terminal (o recarga tu shell):"
echo "  task up"
echo ""
echo "O usa la ruta completa ahora mismo:"
echo "  ./bin/task up"
echo ""
