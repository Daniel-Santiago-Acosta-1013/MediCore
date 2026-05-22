# =============================================================================
# Module: ALB Ingress Controller
# Instala el AWS Load Balancer Controller via Helm con IRSA.
# =============================================================================

# =============================================================================
# Data sources para conectar con el cluster EKS
# =============================================================================

data "aws_eks_cluster" "this" {
  name = var.cluster_name
}

data "aws_eks_cluster_auth" "this" {
  name = var.cluster_name
}

# =============================================================================
# Providers locales para Kubernetes y Helm
# =============================================================================

provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.this.token
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.this.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.this.token
  }
}

variable "cluster_name" {
  description = "Nombre del cluster EKS"
  type        = string
}

variable "cluster_oidc_provider_arn" {
  description = "ARN del OIDC provider del cluster"
  type        = string
}

variable "cluster_oidc_provider_url" {
  description = "URL del OIDC provider del cluster"
  type        = string
}

variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
}

# =============================================================================
# IAM Policy para ALB Controller (oficial de AWS)
# =============================================================================

data "http" "alb_policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.1/docs/install/iam_policy.json"
}

resource "aws_iam_policy" "alb" {
  name   = "${var.cluster_name}-alb-policy"
  policy = data.http.alb_policy.response_body
}

# =============================================================================
# IAM Role + ServiceAccount via IRSA
# =============================================================================

resource "aws_iam_role" "alb" {
  name = "${var.cluster_name}-alb-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = var.cluster_oidc_provider_arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "${replace(var.cluster_oidc_provider_url, "https://", "")}:aud" = "sts.amazonaws.com"
          "${replace(var.cluster_oidc_provider_url, "https://", "")}:sub" = "system:serviceaccount:kube-system:aws-load-balancer-controller"
        }
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "alb" {
  policy_arn = aws_iam_policy.alb.arn
  role       = aws_iam_role.alb.name
}

resource "aws_iam_role_policy" "alb_ec2_security_groups_for_vpc" {
  name = "${var.cluster_name}-alb-ec2-security-groups-for-vpc"
  role = aws_iam_role.alb.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "ec2:GetSecurityGroupsForVpc"
      Resource = "*"
    }]
  })
}

# =============================================================================
# Helm Release: AWS Load Balancer Controller
# =============================================================================

resource "helm_release" "alb" {
  name       = "aws-load-balancer-controller"
  namespace  = "kube-system"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.8.1"

  set {
    name  = "clusterName"
    value = var.cluster_name
  }

  set {
    name  = "serviceAccount.create"
    value = "true"
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = aws_iam_role.alb.arn
  }

  set {
    name  = "vpcId"
    value = var.vpc_id
  }

  set {
    name  = "region"
    value = var.aws_region
  }

  depends_on = [
    aws_iam_role_policy_attachment.alb,
    aws_iam_role_policy.alb_ec2_security_groups_for_vpc,
  ]
}

# =============================================================================
# Outputs
# =============================================================================

output "service_account_name" {
  value = "aws-load-balancer-controller"
}
