# =============================================================================
# Module: Aurora PostgreSQL
# Blueprint reutilizable para cluster RDS Aurora PostgreSQL.
# =============================================================================

variable "identifier" {
  description = "Identificador del cluster Aurora"
  type        = string
}

variable "engine_version" {
  description = "Versión de Aurora PostgreSQL"
  type        = string
  default     = "16.4"
}

variable "instance_class" {
  description = "Clase de instancia Aurora"
  type        = string
  default     = "db.t4g.medium"
}

variable "instance_count" {
  description = "Cantidad de instancias dentro del cluster Aurora"
  type        = number
  default     = 1
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
  description = "Security groups permitidos para acceder a Aurora"
  type        = list(string)
  default     = []
}

# =============================================================================
# Security Group para Aurora
# =============================================================================

resource "aws_security_group" "rds" {
  name_prefix = "${var.identifier}-aurora-"
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
    Name = "${var.identifier}-aurora-sg"
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
# Cluster Aurora PostgreSQL
# =============================================================================

resource "aws_rds_cluster" "this" {
  cluster_identifier     = var.identifier
  engine                 = "aurora-postgresql"
  engine_version         = var.engine_version
  database_name          = var.db_name
  master_username        = var.username
  master_password        = random_password.this.result
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  port                   = 5432
  storage_encrypted      = true
  deletion_protection    = false
  skip_final_snapshot    = true
  apply_immediately      = true

  backup_retention_period      = 7
  preferred_maintenance_window = "Mon:03:00-Mon:04:00"
  preferred_backup_window      = "04:00-05:00"

  tags = merge(var.tags, {
    Name = var.identifier
  })
}

resource "aws_rds_cluster_instance" "this" {
  count               = var.instance_count
  identifier          = "${var.identifier}-${count.index + 1}"
  cluster_identifier  = aws_rds_cluster.this.id
  engine              = aws_rds_cluster.this.engine
  engine_version      = aws_rds_cluster.this.engine_version
  instance_class      = var.instance_class
  publicly_accessible = false

  tags = merge(var.tags, {
    Name = "${var.identifier}-${count.index + 1}"
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
  value = aws_rds_cluster.this.endpoint
}

output "reader_endpoint" {
  value = aws_rds_cluster.this.reader_endpoint
}

output "port" {
  value = aws_rds_cluster.this.port
}

output "db_name" {
  value = aws_rds_cluster.this.database_name
}

output "username" {
  value = aws_rds_cluster.this.master_username
}

output "password" {
  value     = random_password.this.result
  sensitive = true
}

output "security_group_id" {
  value = aws_security_group.rds.id
}
