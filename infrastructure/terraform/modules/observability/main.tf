# =============================================================================
# Module: Observability
# Instala kube-prometheus-stack en EKS para metricas de app y cluster.
# =============================================================================

data "aws_eks_cluster" "this" {
  name = var.cluster_name
}

data "aws_eks_cluster_auth" "this" {
  name = var.cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.this.token
}

provider "helm" {
  kubernetes = {
    host                   = data.aws_eks_cluster.this.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.this.token
  }
}

variable "cluster_name" {
  description = "Nombre del cluster EKS"
  type        = string
}

variable "aws_region" {
  description = "Region AWS"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Entorno"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "medicore"
}

variable "tags" {
  description = "Tags comunes"
  type        = map(string)
  default     = {}
}

variable "namespace" {
  description = "Namespace de observabilidad"
  type        = string
  default     = "medicore-monitoring-env-dev"
}

resource "kubernetes_namespace_v1" "observability" {
  metadata {
    name = var.namespace

    labels = {
      "app.kubernetes.io/name"       = "medicore-observability"
      "app.kubernetes.io/part-of"    = "medicore"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }
}

resource "helm_release" "kube_prometheus_stack" {
  name       = "medicore-observability"
  namespace  = kubernetes_namespace_v1.observability.metadata[0].name
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "85.1.3"
  timeout    = 900
  wait       = true

  values = [
    yamlencode({
      grafana = {
        enabled                  = true
        defaultDashboardsEnabled = false
        adminPassword            = "medicore"
        persistence = {
          enabled = false
        }
        sidecar = {
          dashboards = {
            enabled          = true
            label            = "grafana_dashboard"
            labelValue       = "1"
            folderAnnotation = "grafana_folder"
            searchNamespace  = "ALL"
            provider = {
              allowUiUpdates  = true
              disableDeletion = false
            }
          }
        }
        ingress = {
          enabled = false
        }
      }

      prometheus = {
        prometheusSpec = {
          retention     = "6h"
          retentionSize = "1GB"
          storageSpec = {
            emptyDir = {
              medium = "Memory"
            }
          }
          serviceMonitorSelectorNilUsesHelmValues = false
          serviceMonitorSelector                  = {}
          podMonitorSelectorNilUsesHelmValues     = false
          podMonitorSelector                      = {}
          ruleSelectorNilUsesHelmValues           = false
          ruleSelector                            = {}
          resources = {
            requests = {
              memory = "512Mi"
              cpu    = "250m"
            }
            limits = {
              memory = "1Gi"
              cpu    = "750m"
            }
          }
        }
      }

      alertmanager = {
        enabled = false
      }

      "kube-state-metrics" = {
        enabled = true
      }

      nodeExporter = {
        enabled = false
      }

      "prometheus-node-exporter" = {
        enabled = false
      }
    })
  ]
}

locals {
  dashboard_tags = ["medicore", "errors"]

  backend_dashboard = {
    uid           = "medicore-backend"
    title         = "MediCore - Backend API"
    schemaVersion = 39
    version       = 2
    refresh       = "15s"
    timezone      = "browser"
    tags          = concat(local.dashboard_tags, ["backend"])
    time          = { from = "now-1h", to = "now" }
    panels = [
      {
        id      = 1
        type    = "stat"
        title   = "API Errors 15m"
        gridPos = { h = 4, w = 6, x = 0, y = 0 }
        targets = [{ expr = "sum(increase(medicore_api_errors_total{endpoint!=\"metrics\"}[15m])) or vector(0)", legendFormat = "errors" }]
      },
      {
        id      = 2
        type    = "stat"
        title   = "Unhandled Exceptions 15m"
        gridPos = { h = 4, w = 6, x = 6, y = 0 }
        targets = [{ expr = "sum(increase(medicore_api_exceptions_total[15m])) or vector(0)", legendFormat = "exceptions" }]
      },
      {
        id      = 3
        type    = "stat"
        title   = "Auth Failures 15m"
        gridPos = { h = 4, w = 6, x = 12, y = 0 }
        targets = [{ expr = "sum(increase(medicore_auth_failures_total[15m])) or vector(0)", legendFormat = "auth failures" }]
      },
      {
        id      = 4
        type    = "stat"
        title   = "DB Errors 15m"
        gridPos = { h = 4, w = 6, x = 18, y = 0 }
        targets = [{ expr = "sum(increase(medicore_db_errors_total[15m])) or vector(0)", legendFormat = "db errors" }]
      },
      {
        id      = 5
        type    = "timeseries"
        title   = "API Errors by Module and Type"
        gridPos = { h = 8, w = 12, x = 0, y = 4 }
        targets = [{ expr = "sum by (module, error_type) (rate(medicore_api_errors_total{endpoint!=\"metrics\"}[5m])) or on() vector(0)", legendFormat = "{{module}} / {{error_type}}" }]
      },
      {
        id          = 6
        type        = "timeseries"
        title       = "DB p95 Duration"
        gridPos     = { h = 8, w = 12, x = 12, y = 4 }
        targets     = [{ expr = "(histogram_quantile(0.95, sum by (le, module, operation) (rate(medicore_db_operation_duration_seconds_bucket[5m]))) and on(module, operation) (sum by (module, operation) (rate(medicore_db_operation_duration_seconds_count[5m])) > 0)) or on() vector(0)", legendFormat = "{{module}}/{{operation}}" }]
        fieldConfig = { defaults = { unit = "s" }, overrides = [] }
      }
    ]
  }

  frontend_dashboard = {
    uid           = "medicore-frontend"
    title         = "MediCore - Frontend"
    schemaVersion = 39
    version       = 2
    refresh       = "15s"
    timezone      = "browser"
    tags          = concat(local.dashboard_tags, ["frontend"])
    time          = { from = "now-1h", to = "now" }
    panels = [
      {
        id      = 1
        type    = "stat"
        title   = "Frontend Errors 15m"
        gridPos = { h = 4, w = 6, x = 0, y = 0 }
        targets = [{ expr = "sum(increase(medicore_frontend_errors_total[15m])) or vector(0)", legendFormat = "ui errors" }]
      },
      {
        id      = 2
        type    = "stat"
        title   = "API Errors Seen by Frontend 15m"
        gridPos = { h = 4, w = 6, x = 6, y = 0 }
        targets = [{ expr = "sum(increase(medicore_frontend_api_errors_total[15m])) or vector(0)", legendFormat = "api errors" }]
      },
      {
        id      = 3
        type    = "stat"
        title   = "Error/Warning Toasts 15m"
        gridPos = { h = 4, w = 6, x = 12, y = 0 }
        targets = [{ expr = "sum(increase(medicore_frontend_toasts_total{type=~\"error|warning\"}[15m])) or vector(0)", legendFormat = "toasts" }]
      },
      {
        id      = 4
        type    = "timeseries"
        title   = "Frontend Errors by Route and Source"
        gridPos = { h = 8, w = 12, x = 0, y = 4 }
        targets = [{ expr = "sum by (route, source, error_type) (rate(medicore_frontend_errors_total[5m])) or on() vector(0)", legendFormat = "{{route}} / {{source}} / {{error_type}}" }]
      },
      {
        id          = 5
        type        = "timeseries"
        title       = "Frontend API p95 Duration"
        gridPos     = { h = 8, w = 12, x = 12, y = 4 }
        targets     = [{ expr = "(histogram_quantile(0.95, sum by (le, route, method) (rate(medicore_frontend_api_request_duration_seconds_bucket[5m]))) and on(route, method) (sum by (route, method) (rate(medicore_frontend_api_request_duration_seconds_count[5m])) > 0)) or on() vector(0)", legendFormat = "{{method}} {{route}}" }]
        fieldConfig = { defaults = { unit = "s" }, overrides = [] }
      }
    ]
  }

  cluster_dashboard = {
    uid           = "medicore-cluster"
    title         = "MediCore - Kubernetes Cluster"
    schemaVersion = 39
    version       = 2
    refresh       = "15s"
    timezone      = "browser"
    tags          = concat(local.dashboard_tags, ["kubernetes"])
    time          = { from = "now-1h", to = "now" }
    panels = [
      {
        id      = 1
        type    = "stat"
        title   = "Pods Not Running"
        gridPos = { h = 4, w = 6, x = 0, y = 0 }
        targets = [{ expr = "sum(kube_pod_status_phase{namespace=\"medicore-env-dev\", phase!=\"Running\", phase!=\"Succeeded\"}) or vector(0)", legendFormat = "not running" }]
      },
      {
        id      = 2
        type    = "stat"
        title   = "Restarts 15m"
        gridPos = { h = 4, w = 6, x = 6, y = 0 }
        targets = [{ expr = "sum(increase(kube_pod_container_status_restarts_total{namespace=\"medicore-env-dev\"}[15m])) or vector(0)", legendFormat = "restarts" }]
      },
      {
        id      = 3
        type    = "stat"
        title   = "Unavailable Replicas"
        gridPos = { h = 4, w = 6, x = 12, y = 0 }
        targets = [{ expr = "sum(kube_deployment_status_replicas_unavailable{namespace=\"medicore-env-dev\"}) or vector(0)", legendFormat = "unavailable" }]
      },
      {
        id      = 4
        type    = "timeseries"
        title   = "CrashLoopBackOff / ImagePullBackOff"
        gridPos = { h = 8, w = 12, x = 0, y = 4 }
        targets = [{ expr = "sum by (pod, reason) (kube_pod_container_status_waiting_reason{namespace=\"medicore-env-dev\", reason=~\"CrashLoopBackOff|ImagePullBackOff|ErrImagePull\"}) or on() vector(0)", legendFormat = "{{pod}} / {{reason}}" }]
      },
      {
        id      = 5
        type    = "timeseries"
        title   = "Restarts by Pod"
        gridPos = { h = 8, w = 12, x = 12, y = 4 }
        targets = [{ expr = "sum by (pod) (increase(kube_pod_container_status_restarts_total{namespace=\"medicore-env-dev\"}[15m])) or on() vector(0)", legendFormat = "{{pod}}" }]
      }
    ]
  }

  dashboards = {
    medicore-backend-dashboard = {
      filename = "medicore-backend-dashboard.json"
      content  = local.backend_dashboard
    }
    medicore-frontend-dashboard = {
      filename = "medicore-frontend-dashboard.json"
      content  = local.frontend_dashboard
    }
    medicore-cluster-dashboard = {
      filename = "medicore-cluster-dashboard.json"
      content  = local.cluster_dashboard
    }
  }
}

resource "kubernetes_config_map_v1" "dashboards" {
  for_each = local.dashboards

  metadata {
    name      = each.key
    namespace = kubernetes_namespace_v1.observability.metadata[0].name

    labels = {
      grafana_dashboard = "1"
    }

    annotations = {
      grafana_folder = "MediCore"
    }
  }

  data = {
    (each.value.filename) = jsonencode(each.value.content)
  }

  depends_on = [helm_release.kube_prometheus_stack]
}

output "namespace" {
  value = kubernetes_namespace_v1.observability.metadata[0].name
}
