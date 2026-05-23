include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/observability"
}

dependency "eks" {
  config_path = "../eks"

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    cluster_name = "medicore-eks-prod"
  }
}

inputs = {
  cluster_name = dependency.eks.outputs.cluster_name
  namespace    = "medicore-monitoring-env-dev"
  tags         = include.root.inputs.tags
}
