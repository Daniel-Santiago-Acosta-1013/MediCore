include "root" {
  path   = find_in_parent_folders("root.hcl")
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/ecr"
}

inputs = {
  repositories = [
    "medicore-api",
    "medicore-frontend",
  ]
  tags = include.root.inputs.tags
}
