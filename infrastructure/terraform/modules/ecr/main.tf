# =============================================================================
# Module: ECR
# Blueprint reutilizable para repositorios de contenedores.
# =============================================================================

variable "repositories" {
  description = "Mapa de nombres de repositorio ECR"
  type        = list(string)
}

# =============================================================================
# Repositorios ECR
# =============================================================================

resource "aws_ecr_repository" "this" {
  for_each = toset(var.repositories)

  name                 = each.value
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true

  tags = merge(var.tags, {
    Name = each.value
  })
}

# =============================================================================
# Lifecycle Policy: mantener solo las últimas 30 imágenes
# =============================================================================

resource "aws_ecr_lifecycle_policy" "this" {
  for_each = aws_ecr_repository.this

  repository = each.value.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 30 images"
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 30
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# =============================================================================
# Outputs
# =============================================================================

output "repository_urls" {
  description = "URLs de los repositorios ECR"
  value       = { for name, repo in aws_ecr_repository.this : name => repo.repository_url }
}

output "repository_arns" {
  description = "ARNs de los repositorios ECR"
  value       = { for name, repo in aws_ecr_repository.this : name => repo.arn }
}
