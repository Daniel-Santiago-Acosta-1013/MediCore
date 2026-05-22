include "root" {
  path   = find_in_parent_folders()
  expose = true
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "${get_repo_root()}/infrastructure/terraform/modules/iam-github-oidc"
}

inputs = {
  role_name       = "medicore-github-actions-role"
  github_org      = "Daniel-Santiago-Acosta-1013"
  github_repo     = "MediCore"
  github_branches = ["main", "develop"]
  tags = include.root.inputs.tags
}
