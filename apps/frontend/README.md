# MediCore Frontend

Frontend de MediCore — Sistema de gestión hospitalaria.

## Stack

- React 18 + TypeScript
- Vite 5
- React Router DOM
- CSS puro

## Requisitos

- Node.js 18+
- Backend de MediCore corriendo en `http://localhost:8000`

## Instalación

```bash
npm install
```

## Variables de entorno

```bash
cp .env.example .env
```

`VITE_API_URL` apunta al backend. Por defecto `/api` (proxy de Vite en desarrollo).

## Comandos

```bash
npm run dev      # Servidor de desarrollo
npm run build    # Build de producción
npm run preview  # Preview del build
npm run lint     # Chequeo de tipos
```

## Tests E2E

Requiere backend y frontend corriendo.

```bash
# Instalar browsers de Playwright (primera vez)
npx playwright install chromium

# Ejecutar tests E2E
npx playwright test --workers=1

# O con Task
task test:e2e
```

## Estructura

```
src/
  api/          # Cliente HTTP + endpoints
  components/   # Componentes reutilizables (Button/, Input/, etc.)
  layouts/      # Layouts de página
  pages/        # Vistas por ruta
  routes/       # Definición de rutas
  stores/       # Contextos de estado
  styles/       # Estilos globales
  types/        # Tipos TypeScript
  utils/        # Utilidades
```

## Licencia

MIT
