# Standard outputs for public or non-sensitive information
output "primary_bucket_name" {
  description = "The name of the primary S3 bucket"
  value       = aws_s3_bucket.main_bucket.id
}

output "primary_bucket_arn" {
  description = "The ARN of the primary S3 bucket"
  value       = aws_s3_bucket.main_bucket.arn
}

/* output "secondary_bucket_name" {
  description = "The name of the secondary S3 bucket"
  value       = aws_s3_bucket.secondary.id
}

output "secondary_bucket_arn" {
  description = "The ARN of the secondary S3 bucket"
  value       = aws_s3_bucket.secondary.arn
} */


output "secrets_manager_secret_arn" {
  description = "The ARN of the secret stored in Secrets Manager"
  value       = aws_secretsmanager_secret.app_secret.arn
}

# DEMO: Sensitive Output
# If `sensitive = true` is omitted, Terraform will throw an error because it contains a sensitive variable.
output "db_password_raw" {
  description = "The database password output (will be masked in terminal)"
  value       = var.db_password
  sensitive   = true
}
