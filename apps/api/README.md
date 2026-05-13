# MediCore API

Backend realista para gestionar operaciones básicas de un hospital.

## Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQL puro (psycopg 3)
- Pydantic v2
- JWT
- Sqitch (migraciones)
- Docker / Docker Compose
- Pytest
- **uv** (gestor de dependencias)
- **Task** (runner de tareas)

> **Nota:** Este proyecto utiliza `uv` de manera precisa para la gestión de dependencias y `Task` para automatizar flujos de trabajo.

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose

> **Task** se instala automáticamente dentro del proyecto (ver abajo). No necesitás instalarlo globalmente.

### Instalar Task localmente (oficial)

Task se instala localmente en `./bin/task` usando el script oficial. No requiere `sudo` ni afecta tu sistema.

```bash
# Instalar Task localmente (una sola vez por proyecto)
./scripts/install-task.sh

# Verificar
task --version
```

> El script configura automáticamente tu shell para que `task` funcione desde cualquier lugar. Solo tenés que abrir una nueva terminal o recargar tu shell (`source ~/.bashrc` o `source ~/.zshrc`).

## Levantar el proyecto (modo automático)

```bash
# Levanta contenedores existentes (rápido, sin rebuild)
task up

# O si cambiaste el Dockerfile, pyproject.toml, scripts o db:
task up:build
```

La API estará disponible en: http://localhost:8000

### ¿Qué hace `task up`?

1. Levanta los contenedores (`docker compose up -d`).
2. Espera a que PostgreSQL esté sano.
3. Espera a que la API responda en `/health`.
4. Las migraciones de Sqitch se aplican **automáticamente** dentro del contenedor via `entrypoint.sh`.

> **Nota:** `task up` no fuerza `docker build` cada vez. Si modificaste el `Dockerfile`, `pyproject.toml`, scripts o la carpeta `db/`, usá `task up:build`.

## Tareas disponibles (Taskfile)

### Infraestructura

| Comando | Descripción |
|---------|-------------|
| `task up` | Levanta API + DB (rápido, sin rebuild) |
| `task up:build` | Build + levanta API + DB + migraciones automáticas |
| `task down` | Detiene y elimina contenedores |
| `task restart` | Reinicia la API y espera a que responda |
| `task logs` | Logs de todos los servicios |
| `task api:logs` | Logs solo de la API |
| `task db:logs` | Logs solo de PostgreSQL |
| `task clean` | Limpia contenedores, volúmenes y entorno virtual |

### Base de datos (Sqitch)

| Comando | Descripción |
|---------|-------------|
| `task db:migrate` | Aplica migraciones (`sqitch deploy`) |
| `task db:revert` | Revierte migraciones (`sqitch revert`) |
| `task db:verify` | Verifica estado (`sqitch verify`) |
| `task db:status` | Muestra estado detallado de migraciones |
| `task db:reset` | **Revierte todo y vuelve a aplicar** (¡cuidado con los datos!) |
| `task db:shell` | Abre `psql` interactivo en el contenedor |

### Tests

| Comando | Descripción |
|---------|-------------|
| `task test` | Corre tests dentro del contenedor Docker |
| `task test:local` | Corre tests localmente con `uv run pytest` |
| `task test:cov` | Tests con reporte de cobertura |
| `task test:api` | **Tests end-to-end automaticos** con Schemathesis (requiere API corriendo) |

### Pipeline local de dependencias

| Comando | Descripción |
|---------|-------------|
| `task deps:pipeline` | **Pipeline completo**: lock → sync → audit → outdated |
| `task deps:lock` | Genera/actualiza `uv.lock` |
| `task deps:sync` | Sincroniza el `.venv` con `uv.lock` |
| `task deps:upgrade` | Actualiza todas las dependencias compatibles |
| `task deps:audit` | Audita vulnerabilidades con `uv run pip-audit` |
| `task deps:outdated` | Muestra paquetes con versiones más recientes |
| `task deps:export` | Exporta a `requirements.txt` |
| `task deps:clean` | Elimina `.venv` y caché de uv |

### Calidad de código

| Comando | Descripción |
|---------|-------------|
| `task lint` | Linting con `ruff` (si está instalado) |
| `task format` | Formateo con `ruff` (si está instalado) |

### Utilidades

| Comando | Descripción |
|---------|-------------|
| `task api:shell` | Abre un shell bash dentro del contenedor API |
| `task api:health` | Verifica el endpoint `/health` |

## Gestión de dependencias con uv

Las dependencias están declaradas en `pyproject.toml` y bloqueadas en `uv.lock`.

### Pipeline manual (sin Task)

```bash
# Sincronizar entorno
uv sync

# Pipeline completo de dependencias
./scripts/deps-pipeline.sh
```

### Agregar una dependencia

```bash
uv add <paquete>
```

### Agregar dependencia de desarrollo

```bash
uv add --group dev <paquete>
```

## Migraciones con Sqitch

Las migraciones se aplican **automáticamente** cada vez que el contenedor de la API arranca, gracias a `scripts/entrypoint.sh`.

Si necesitas correrlas manualmente (por ejemplo, si editaste el entrypoint para omitir el auto-deploy):

```bash
# Aplicar
task db:migrate

# Revertir
task db:revert

# Verificar
task db:verify

# Estado
task db:status
```

## Variables de entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://medicore:secret@db:5432/medicore` |
| `POSTGRES_USER` | Usuario de PostgreSQL | `medicore` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | `secret` |
| `POSTGRES_DB` | Nombre de la base de datos | `medicore` |
| `POSTGRES_HOST` | Host de PostgreSQL | `db` |
| `POSTGRES_PORT` | Puerto de PostgreSQL | `5432` |
| `SECRET_KEY` | Clave secreta para JWT | `super-secret-key-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de expiración del token | `30` |
| `ALGORITHM` | Algoritmo JWT | `HS256` |

## Endpoints iniciales

- `GET /health` — Health check
- `POST /auth/register` — Registro de usuario
- `POST /auth/login` — Login de usuario (OAuth2)
- `GET /auth/me` — Obtener usuario autenticado

## Arquitectura

```
app/
  main.py
  core/          # Configuración, DB, seguridad, permisos
  modules/       # Módulos del dominio (auth, users, patients, etc.)
    auth/
      router.py      # Rutas FastAPI
      schemas.py     # Pydantic models
      service.py     # Lógica de negocio
      repository.py  # SQL puro con psycopg
```

- **Routers**: Solo reciben requests y devuelven responses.
- **Services**: Contienen la lógica de negocio. Sin SQL directo.
- **Repositories**: Contienen SQL puro. Único lugar con queries.

## Notas

- No se usa ORM. Toda interacción con la base de datos se hace con SQL explícito usando psycopg 3.
- Las transacciones se manejan explícitamente en repositories y services.
- Los parámetros de queries siempre usan placeholders de psycopg (`%s`), nunca concatenación de strings.
- El gestor de dependencias es **uv**. No usar `pip install` directamente; usar siempre `uv add` o `uv sync`.
- El runner de tareas es **Task** (`taskfile.dev`). No es necesario recordar comandos largos de Docker o Sqitch.
