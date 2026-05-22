# =============================================================================
# Module: RDS PostgreSQL
# Blueprint reutilizable para instancia RDS.
# =============================================================================

variable "identifier" {
  description = "Identificador de la instancia RDS"
  type        = string
}

variable "engine_version" {
  description = "Versión de PostgreSQL"
  type        = string
  default     = "16.4"
}

variable "instance_class" {
  description = "Clase de instancia RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Almacenamiento en GB"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "username" {
  description = "Usuario administrador"
  type        = string
  default     = "medicore"
}

variable "vpc_id" {
  description = "ID de la VPC"
  type        = string
}

variable "subnet_ids" {
  description = "IDs de subnets privadas para el subnet group"
  type        = list(string)
}

variable "allowed_security_group_ids" {
  description = "Security groups permitidos para acceder a RDS"
  type        = list(string)
  default     = []
}

# =============================================================================
# Security Group para RDS
# =============================================================================

resource "aws_security_group" "rds" {
  name_prefix = "${var.identifier}-rds-"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = var.allowed_security_group_ids
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.identifier}-rds-sg"
  })

  lifecycle {
    create_before_destroy = true
  }
}

# =============================================================================
# Subnet Group
# =============================================================================

resource "aws_db_subnet_group" "this" {
  name       = var.identifier
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, {
    Name = var.identifier
  })
}

# =============================================================================
# Instancia RDS
# =============================================================================

resource "aws_db_instance" "this" {
  identifier             = var.identifier
  engine                 = "postgres"
  engine_version         = var.engine_version
  instance_class         = var.instance_class
  allocated_storage      = var.allocated_storage
  storage_type           = "gp2"
  db_name                = var.db_name
  username               = var.username
  password               = random_password.this.result
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
  deletion_protection    = false
  storage_encrypted      = true

  backup_retention_period = 7
  maintenance_window      = "Mon:03:00-Mon:04:00"
  backup_window           = "04:00-05:00"

  tags = merge(var.tags, {
    Name = var.identifier
  })
}

# =============================================================================
# Password aleatoria
# =============================================================================

resource "random_password" "this" {
  length  = 32
  special = false
}

# =============================================================================
# Outputs
# =============================================================================

output "endpoint" {
  value = aws_db_instance.this.endpoint
}

output "db_name" {
  value = aws_db_instance.this.db_name
}

output "username" {
  value = aws_db_instance.this.username
}

output "password" {
  value     = aws_db_instance.this.password
  sensitive = true
}

output "security_group_id" {
  value = aws_security_group.rds.id
}
