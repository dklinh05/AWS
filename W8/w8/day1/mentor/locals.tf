locals {
  # Prefix to construct resource names dynamically
  name_prefix = "${var.bucket_prefix}-${var.environment}"

  # Standard tags to apply to all taggable resources
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = "Mentor-AWS-Training"
    Owner       = "Mentor-Team"
  }
}
