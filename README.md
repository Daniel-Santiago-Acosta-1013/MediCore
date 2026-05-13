# MediCore

Sistema de gestión hospitalaria. Monorepo con frontend React, backend FastAPI e infraestructura Kubernetes local gestionada como código.

## Stack

| Capa | Tecnología |
|------|-----------|
| Frontend | React 18 + TypeScript + Vite 5 |
| Backend | Python 3.12 + FastAPI + Pydantic v2 + JWT |
| Base de datos | PostgreSQL 16 (Docker nativo, fuera del cluster) |
| Migraciones | Sqitch |
| Infraestructura | Kubernetes (k3d) + Kustomize + Traefik |
| Dependencias API | uv |
| Runner de tareas | Task (go-task) |

## Estructura

```
MediCore/
├── apps/
│   ├── api/              # Backend FastAPI
│   └── frontend/         # Frontend React + Vite
├── infrastructure/
│   └── k8s/              # Manifiestos Kubernetes (Kustomize)
│       ├── base/         # Recursos reutilizables
│       └── overlays/
│           └── local/    # Configuración de ambiente local
├── docker-compose.db.yml # PostgreSQL persistente fuera del cluster
└── Taskfile.yml          # Automatización unificada
```

## Requisitos previos

- Docker
- k3d
- kubectl
- Task (`brew install go-task`)

## Levantar todo

```bash
# Levanta PostgreSQL + cluster k3d + aplica infraestructura
# También carga las imágenes locales al cluster
task cluster:up
```

Esto ejecuta secuencialmente:
1. `task db:up` — Levanta PostgreSQL en Docker nativo (`localhost:5432`)
2. `task build:api` y `task build:frontend` — Construye imágenes Docker y las carga al cluster
3. `task infra:apply` — Aplica manifiestos Kubernetes vía Kustomize

## URLs de acceso

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost/ |
| API Docs (Swagger) | http://localhost/api/docs |
| API Health | http://localhost/api/health |

## Comandos esenciales

```bash
task --list                 # Ver todas las tareas disponibles

task db:up                  # Levantar PostgreSQL
task db:down                # Detener PostgreSQL (conserva datos)
task db:destroy             # Destruir PostgreSQL y borrar datos
task db:shell               # Abrir psql

task cluster:up             # Levantar DB + cluster + aplicar infra
task cluster:down           # Destruir SOLO el cluster (la DB sigue)
task cluster:destroy        # Destruir TODO (cluster + DB + datos)
task cluster:status         # Estado de nodos y pods

task build:api              # Build + importar imagen de la API
task build:frontend         # Build + importar imagen del frontend

task infra:apply            # Aplicar manifiestos Kubernetes
task infra:destroy          # Eliminar recursos de MediCore del cluster

task k9s                    # Abrir k9s en medicore-api
task k9s:all                # Abrir k9s en todos los namespaces

task logs:api               # Logs del API Gateway
task logs:frontend          # Logs del Frontend

task test:api               # Tests unitarios del API (local con uv)
task test:frontend          # Lint del frontend
```

## Arquitectura de despliegue local

```
┌─────────────────────────────────────────────────────────────┐
│  Tu máquina                                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Cluster k3d (Kubernetes)                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐   │   │
│  │  │ Frontend Pod │  │  API Pod     │  │ Ingress   │   │   │
│  │  │ (React)      │  │  (FastAPI)   │  │ (Traefik)  │   │   │
│  │  │ Port: 80     │  │  Port: 8000  │  │ Port: 80  │   │   │
│  │  └──────┬───────┘  └───────┬──────┘  └─────┬─────┘   │   │
│  │         └──────────────────┴────────────────┘        │   │
│  │                            │                         │   │
│  │                   localhost:80                       │   │
│  └────────────────────────────┼─────────────────────────┘   │
│                               │                             │
│  ┌────────────────────────────┼─────────────────────────┐   │
│  │  Docker nativo             │                         │   │
│  │  ┌─────────────────────────┘                         │   │
│  │  │ PostgreSQL                                        │   │
│  │  │ localhost:5432                                    │   │
│  │  └───────────────────────────────────────────────────┘   │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Principios clave

- **GitOps**: Git es la única fuente de verdad. Los manifiestos definen el estado deseado.
- **DB fuera del cluster**: PostgreSQL corre en Docker nativo para persistir datos entre destrucciones del cluster.
- **Imágenes locales**: Las imágenes de API y frontend se construyen localmente y se importan al cluster con `k3d image import`.
- **Kustomize**: `base/` contiene manifiestos genéricos; `overlays/local/` aplica parches específicos para desarrollo (recursos reducidos, prefijos/sufijos).
- **Enrutamiento**: Traefik enruta `localhost/` al frontend y `localhost/api/*` al backend. Un `Middleware` strippea el prefijo `/api` antes de llegar a FastAPI.

## Notas

- No usar `pip install` en el API; usar `uv add` o `uv sync`.
- Las migraciones de Sqitch se aplican automáticamente en el `entrypoint` del contenedor de la API.
- Para forzar un rebuild completo: `task cluster:destroy && task cluster:up`.
