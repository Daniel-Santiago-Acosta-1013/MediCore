include "root" {
  path   = find_in_parent_folders()
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/alb-ingress-controller"
}

dependency "eks" {
  config_path = "../eks"
}

dependency "vpc" {
  config_path = "../vpc"
}

inputs = {
  cluster_name              = include.root.inputs.cluster_name
  cluster_oidc_provider_arn = dependency.eks.outputs.oidc_provider_arn
  cluster_oidc_provider_url = dependency.eks.outputs.oidc_provider_url
  vpc_id                    = dependency.vpc.outputs.vpc_id
  tags = include.root.inputs.tags
}
