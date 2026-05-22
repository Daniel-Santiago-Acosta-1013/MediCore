# =============================================================================
# Module: IAM GitHub OIDC
# Blueprint para autenticar GitHub Actions en AWS sin credenciales de larga
# duración, usando OIDC (IRSA para CI/CD).
# =============================================================================

variable "role_name" {
  description = "Nombre del IAM Role para GitHub Actions"
  type        = string
}

variable "github_org" {
  description = "Organización o usuario de GitHub"
  type        = string
}

variable "github_repo" {
  description = "Nombre del repositorio de GitHub"
  type        = string
}

variable "github_branches" {
  description = "Ramas permitidas para asumir el role"
  type        = list(string)
  default     = ["main", "develop"]
}

# =============================================================================
# OIDC Identity Provider para GitHub Actions
# =============================================================================

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = ["sts.amazonaws.com"]

  thumbprint_list = [
    "a031c46782e6e6c662c2c87c76da9aa62ccabd8e",
    "6938fd4e98bab7fa3867c43166814f670a51d28e"
  ]

  tags = var.tags
}

# =============================================================================
# IAM Role para GitHub Actions
# =============================================================================

resource "aws_iam_role" "github_actions" {
  name = var.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = [
            for branch in var.github_branches : "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${branch}"
          ]
        }
      }
    }]
  })

  tags = var.tags
}

# =============================================================================
# Policy inline: permisos mínimos para CI/CD
# - ECR: push/pull images
# - EKS: update-kubeconfig, describe cluster
# - EC2: describir VPC/Subnets/Security Groups (para validaciones)
# =============================================================================

resource "aws_iam_role_policy" "cicd" {
  name = "${var.role_name}-cicd-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ECRAccess"
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = "*"
      },
      {
        Sid    = "EKSAccess"
        Effect = "Allow"
        Action = [
          "eks:DescribeCluster",
          "eks:ListClusters"
        ]
        Resource = "*"
      },
      {
        Sid    = "EC2ReadOnly"
        Effect = "Allow"
        Action = [
          "ec2:DescribeVpcs",
          "ec2:DescribeSubnets",
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeInstances"
        ]
        Resource = "*"
      }
    ]
  })
}

# =============================================================================
# Outputs
# =============================================================================

output "role_arn" {
  description = "ARN del IAM Role para GitHub Actions"
  value       = aws_iam_role.github_actions.arn
}
