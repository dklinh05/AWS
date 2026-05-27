output "cloudfront_url" {
  description = "The public URL of the application served via CloudFront (use this to access the app)"
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "ec2_public_ip" {
  description = "Public IP of the backend EC2 instance"
  value       = aws_instance.studybot.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the backend EC2 instance"
  value       = aws_instance.studybot.public_dns
}

output "s3_docs_bucket" {
  description = "Name of the S3 bucket storing user-uploaded documents"
  value       = aws_s3_bucket.docs.id
}

output "s3_frontend_bucket" {
  description = "Name of the S3 bucket hosting frontend static web assets"
  value       = aws_s3_bucket.frontend.id
}

output "dynamodb_table" {
  description = "Name of the DynamoDB user storage table"
  value       = aws_dynamodb_table.users.name
}
