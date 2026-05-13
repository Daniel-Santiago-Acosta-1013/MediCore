# MediCore - Infrastructure as Code (Kubernetes)

Este directorio contiene toda la definición declarativa de la infraestructura Kubernetes del proyecto **MediCore**, gestionada mediante **Kustomize** y desplegada localmente con **k3d**.

## Estructura del Proyecto

```
infrastructure/k8s/
├── namespaces/
│   └── namespaces.yaml          # Definición de namespaces por dominio
├── base/
│   ├── api-gateway/             # API Gateway - punto de entrada
│   ├── patient-service/         # Microservicio de pacientes
│   └── frontend-app/            # Aplicación web (React/Vue/Angular)
└── overlays/
    └── local/                   # Configuración específica para ambiente local
        ├── patches/             # Parches de recursos por ambiente
        └── ingress.yaml         # Reglas de enrutamiento local
```

## Principios

- **GitOps**: Git es la única fuente de verdad.
- **Kustomize**: Gestión de configuraciones sin templating complejo.
- **Namespacing por dominio**: Separación lógica entre API, Frontend y System.
- **Labels estandarizadas**: Seguimos las recomendaciones de Kubernetes (`app.kubernetes.io/*`).

## Cluster Local

| Propiedad | Valor |
|-----------|-------|
| Nombre | `medicore-dev` |
| Plataforma | k3d (k3s en Docker) |
| Nodos | 1 server + 2 agents |
| Ingress | localhost:80 / localhost:443 |

## Comandos Esenciales

```bash
# Aplicar configuración local completa
kubectl apply -k overlays/local/

# Ver estado de todos los recursos
kubectl get all -n medicore-api
kubectl get all -n medicore-frontend

# Ver logs de un servicio
kubectl logs -n medicore-api deployment/api-gateway -f

# Escalar un servicio manualmente
kubectl scale deployment api-gateway -n medicore-api --replicas=3

# Destruir y recrear cluster
k3d cluster delete medicore-dev
k3d cluster create medicore-dev --servers 1 --agents 2 --port "80:80@loadbalancer" --port "443:443@loadbalancer"
```

## Visualización con k9s

```bash
k9s -n medicore-api
```

Atajos útiles en k9s:
- `:` → Cambiar recurso (pods, deployments, services, ingress)
- `d` → Describe recurso
- `l` → Logs en vivo
- `s` → Shell interactivo en el contenedor
- `y` → Ver manifest YAML
