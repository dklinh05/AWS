terraform {
  # Minimum Terraform version required (supporting native import blocks)
  required_version = ">= 1.5.0"

  # S3 backend configuration for state storage
 /* backend "s3" {
    bucket         = "mentor-terraform-state-bucket"
    key            = "env/dev/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "mentor-terraform-state-lock"
  }
*/

  # AWS Provider requirements
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# AWS provider configuration
provider "aws" {
  region = var.aws_region
}
