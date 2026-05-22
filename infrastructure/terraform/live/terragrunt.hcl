# =============================================================================
# Root Terragrunt Configuration
# Configura el backend remoto S3 + DynamoDB para todos los módulos.
# =============================================================================

remote_state {
  backend = "s3"
  config = {
    bucket         = "medicore-terraform-state-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "medicore-terraform-locks"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# =============================================================================
# Provider AWS común
# =============================================================================

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terragrunt"
    }
  }
}
EOF
}

# =============================================================================
# Variables comunes inyectadas a todos los módulos
# =============================================================================

inputs = {
  aws_region    = "us-east-1"
  environment   = "prod"
  project_name  = "medicore"
  cluster_name  = "medicore-eks-prod"
  tags = {
    Project     = "medicore"
    Environment = "prod"
    ManagedBy   = "terragrunt"
  }
}
