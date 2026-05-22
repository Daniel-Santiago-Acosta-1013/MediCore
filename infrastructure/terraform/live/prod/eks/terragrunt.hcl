include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/eks"
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    vpc_id             = "vpc-00000000000000000"
    private_subnet_ids = ["subnet-00000000000000000", "subnet-11111111111111111"]
  }
}

inputs = {
  cluster_name        = include.root.inputs.cluster_name
  cluster_version     = "1.31"
  vpc_id              = dependency.vpc.outputs.vpc_id
  subnet_ids          = dependency.vpc.outputs.private_subnet_ids
  node_instance_types = ["t3.medium"]
  node_desired_size   = 2
  node_min_size       = 2
  node_max_size       = 4
  tags                = include.root.inputs.tags
}
