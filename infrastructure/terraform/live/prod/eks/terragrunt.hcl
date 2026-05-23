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
  cluster_name    = include.root.inputs.cluster_name
  cluster_version = "1.31"
  vpc_id          = dependency.vpc.outputs.vpc_id
  subnet_ids      = dependency.vpc.outputs.private_subnet_ids
  fargate_profiles = {
    app = {
      namespace = "medicore-env-dev"
    }
    coredns = {
      namespace = "kube-system"
      labels = {
        k8s-app = "kube-dns"
      }
    }
    aws_load_balancer_controller = {
      namespace = "kube-system"
      labels = {
        "app.kubernetes.io/name" = "aws-load-balancer-controller"
      }
    }
    observability = {
      namespace = "medicore-monitoring-env-dev"
    }
  }
  tags = include.root.inputs.tags
}
