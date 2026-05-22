variable "aws_region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Entorno (prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "medicore"
}

variable "tags" {
  description = "Tags comunes para todos los recursos"
  type        = map(string)
  default     = {}
}
