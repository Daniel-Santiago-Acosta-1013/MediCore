# MediCore

Monorepo de la plataforma MediCore. Contiene API, Frontend e Infraestructura como Código.

## Estructura

```
MediCore/
├── apps/
│   ├── api/                # Backend (Python)
│   └── frontend/           # Frontend (React + Vite)
├── infrastructure/
│   └── k8s/                # Manifiestos Kubernetes (Kustomize)
├── .github/
│   └── workflows/          # CI/CD unificado
├── docker-compose.yml      # Desarrollo local con Docker
└── README.md
```

## Desarrollo Local

### Opción 1: Docker Compose (rápido)

```bash
docker compose up --build
```

- API: http://localhost:8000
- Frontend: http://localhost:3000

### Opción 2: Kubernetes Local (k3d)

Requisitos: Docker, k3d, kubectl

```bash
# Crear cluster
k3d cluster create medicore-dev --servers 1 --agents 2 --port "80:80@loadbalancer" --port "443:443@loadbalancer"

# Aplicar infraestructura
kubectl apply -k infrastructure/k8s/overlays/local/

# Ver estado
k9s -n medicore-api
```

## CI/CD

Cada push a `main` o `develop` dispara:
1. Build de imagen API
2. Build de imagen Frontend
3. Validación de manifiestos K8s

## Enlaces

- Repositorio: `git@github.com:Daniel-Santiago-Acosta-1013/MediCore.git`
