# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "mentor-training-dev-primary-bucket"
resource "aws_s3_bucket" "imported_bucket" {
  bucket              = "mentor-training-dev-primary-bucket"
  force_destroy       = null
  object_lock_enabled = false
  tags = {
    Environment = "dev"
    ManagedBy   = "Terraform"
    Owner       = "Mentor-Team"
    Project     = "Mentor-AWS-Training"
  }
  tags_all = {
    Environment = "dev"
    ManagedBy   = "Terraform"
    Owner       = "Mentor-Team"
    Project     = "Mentor-AWS-Training"
  }
}
