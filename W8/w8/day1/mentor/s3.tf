# Primary S3 Bucket
resource "aws_s3_bucket" "main_bucket" {
  bucket        = "${local.name_prefix}-primary-bucket"
  force_destroy = true # Allow bucket deletion during training cleanup

  tags = local.common_tags
}

# Public Access Block for Primary Bucket
# DEMO: Implicit dependency. This resource implicitly depends on `aws_s3_bucket.primary`
# because it references its attribute `aws_s3_bucket.primary.id`.
resource "aws_s3_bucket_public_access_block" "primary_pab" {
  bucket = aws_s3_bucket.main_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Secondary S3 Bucket
/*resource "aws_s3_bucket" "secondary" {
  bucket        = "${local.name_prefix}-secondary-bucket"
  force_destroy = true

  tags = local.common_tags

  # DEMO: Explicit dependency using `depends_on`.
  # This ensures the secondary bucket is only created after the primary bucket
  # is fully provisioned.
  depends_on = [
    aws_s3_bucket.main_bucket
  ]
} */

# S3 Bucket Object in the Secondary Bucket
# DEMO: Demonstrates both implicit and explicit dependencies.
/* resource "aws_s3_object" "readme_object" {
  bucket       = aws_s3_bucket.secondary.id # Implicit dependency on aws_s3_bucket.secondary
  key          = "README.txt"
  content      = "This is a configuration bucket managed by Terraform."
  content_type = "text/plain"

  tags = local.common_tags

  # DEMO: Explicitly depends on primary bucket's public access block being applied.
  depends_on = [
    aws_s3_bucket_public_access_block.primary_pab
  ]
} */
