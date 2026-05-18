# MediCore

Sistema de gestión hospitalaria. Monorepo con frontend React, backend FastAPI e infraestructura Kubernetes local.

## Stack

| Capa | Tecnología |
|------|------------|
| Frontend | React 18 + TypeScript + Vite |
| Backend | Python 3.12+ + FastAPI + Pydantic |
| Base de datos | PostgreSQL 16 en Docker Compose |
| Infraestructura local | Docker Desktop Kubernetes + Kustomize + Traefik + Metrics Server |
| Pipeline local | Taskfile + Skaffold |

## Flujo local

Taskfile es la entrada operativa del proyecto.
Skaffold construye las imágenes, inyecta tags locales y despliega los manifests renderizados por Kustomize.
Docker Desktop Kubernetes ejecuta el cluster local.

```bash
task cluster:up
```

Ese comando levanta PostgreSQL, valida el cluster local, instala o actualiza Traefik, instala o actualiza Metrics Server y aplica la infraestructura con Skaffold.

## Requisitos

- Docker Desktop con Kubernetes habilitado
- kubectl
- Helm
- Task
- Skaffold
- Kustomize
- k9s opcional para observabilidad

En macOS:

```bash
brew install go-task helm kubectl skaffold kustomize k9s
```

## Comandos

```bash
task db:up                  # Levantar PostgreSQL
task db:down                # Detener PostgreSQL (conserva datos)
task db:destroy             # Destruir PostgreSQL y borrar datos
task db:shell               # Abrir psql

task cluster:up             # Configurar cluster + Traefik + aplicar infra
task cluster:down           # Eliminar recursos de MediCore del cluster
task cluster:destroy        # Destruir TODO (recursos + DB + datos)
task cluster:status         # Estado de nodos y pods

task build:api              # Build imagen de la API
task build:frontend         # Build imagen del frontend

task infra:apply            # Aplicar manifiestos Kubernetes
task infra:destroy          # Eliminar recursos de MediCore del cluster

task k9s                    # Abrir k9s en medicore-api
task k9s:all                # Abrir k9s en todos los namespaces

task logs:api               # Logs del API Gateway
task logs:frontend          # Logs del Frontend

task test:api               # Tests unitarios del API (local con uv)
task test:frontend          # Lint del frontend
```

## URLs locales

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost/ |
| API health | http://localhost/api/health |
| API docs | http://localhost/api/docs |

## Estructura relevante

```text
apps/api/Dockerfile
apps/frontend/Dockerfile
docker-compose.db.yml
skaffold.yaml
Taskfile.yml
infrastructure/k8s/base/
infrastructure/k8s/overlays/local/
```

## Notas de diseño

- PostgreSQL corre fuera del cluster para conservar datos entre redeploys.
- La API se conecta a PostgreSQL desde Kubernetes usando `host.docker.internal`.
- Skaffold usa `push: false` para Docker Desktop Kubernetes.
- Kustomize aplica `namePrefix` y `nameSuffix`; las referencias de Traefik se transforman con `kustomizeconfig.yaml`.
- El HPA queda configurado para API y frontend desde `task cluster:up`, usando CPU como señal de escalado.
- Metrics Server se instala internamente en `kube-system` porque HPA necesita métricas de CPU y memoria.
