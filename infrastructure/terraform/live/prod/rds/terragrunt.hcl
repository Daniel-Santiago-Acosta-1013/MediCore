include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/rds"
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    vpc_id             = "vpc-00000000000000000"
    private_subnet_ids = ["subnet-00000000000000000", "subnet-11111111111111111"]
  }
}

dependency "eks" {
  config_path = "../eks"

  mock_outputs_allowed_terraform_commands = ["init", "validate", "plan", "destroy", "state"]
  mock_outputs = {
    cluster_security_group_id = "sg-00000000000000000"
  }
}

inputs = {
  identifier                 = "medicore-aurora-postgres-prod"
  engine_version             = "16.4"
  instance_class             = "db.t4g.medium"
  instance_count             = 1
  db_name                    = "medicore"
  username                   = "medicore"
  vpc_id                     = dependency.vpc.outputs.vpc_id
  subnet_ids                 = dependency.vpc.outputs.private_subnet_ids
  allowed_security_group_ids = [dependency.eks.outputs.cluster_security_group_id]
  tags                       = include.root.inputs.tags
}
