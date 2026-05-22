include "root" {
  path   = find_in_parent_folders()
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
}

dependency "eks" {
  config_path = "../eks"
}

inputs = {
  identifier             = "medicore-postgres-prod"
  engine_version         = "16.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "medicore"
  username               = "medicore"
  vpc_id                 = dependency.vpc.outputs.vpc_id
  subnet_ids             = dependency.vpc.outputs.private_subnet_ids
  allowed_security_group_ids = [dependency.eks.outputs.cluster_security_group_id]
  tags = include.root.inputs.tags
}
