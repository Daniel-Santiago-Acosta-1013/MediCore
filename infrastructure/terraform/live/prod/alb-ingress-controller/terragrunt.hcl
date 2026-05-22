include "root" {
  path   = find_in_parent_folders("root.hcl")
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

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    oidc_provider_arn = "arn:aws:iam::000000000000:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/mock"
    oidc_provider_url = "https://oidc.eks.us-east-1.amazonaws.com/id/mock"
  }
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    vpc_id = "vpc-00000000000000000"
  }
}

inputs = {
  cluster_name              = include.root.inputs.cluster_name
  cluster_oidc_provider_arn = dependency.eks.outputs.oidc_provider_arn
  cluster_oidc_provider_url = dependency.eks.outputs.oidc_provider_url
  vpc_id                    = dependency.vpc.outputs.vpc_id
  tags                      = include.root.inputs.tags
}
