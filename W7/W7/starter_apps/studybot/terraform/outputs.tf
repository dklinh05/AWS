output "cloudfront_url" {
  description = "The public URL of the application served via CloudFront (use this to access the app)"
  value       = "https://${aws_cloudfront_distribution.main.domain_name}"
}

output "api_gateway_url" {
  description = "Direct HTTPS endpoint of the API Gateway HTTP API"
  value       = aws_apigatewayv2_api.api.api_endpoint
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
