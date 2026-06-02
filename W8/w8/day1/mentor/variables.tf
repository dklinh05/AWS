variable "aws_region" {
  type        = string
  description = "The AWS region to deploy resources in"
  default     = "ap-southeast-1"
}

variable "environment" {
  type        = string
  description = "The environment name (e.g. dev, staging, prod)"
  default     = "dev"
}

variable "bucket_prefix" {
  type        = string
  description = "Prefix for S3 bucket names to ensure global uniqueness"
  default     = "mentor-training"
}

variable "db_password" {
  type        = string
  description = "A sensitive database password example to show secrets handling"
  sensitive   = true
  default     = "SuperSecretPassword123!"
}
