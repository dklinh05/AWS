# ---------------------------------------------------------
# CloudFront Origin Access Control (OAC) for S3
# ---------------------------------------------------------
resource "aws_cloudfront_origin_access_control" "s3_oac" {
  name                              = "${var.project}-s3-oac"
  description                       = "CloudFront OAC for S3 static frontend"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# ---------------------------------------------------------
# CloudFront Distribution
# ---------------------------------------------------------
resource "aws_cloudfront_distribution" "main" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = "PriceClass_100" # Cheapest price class, ideal for hackathons

  # Origin 1: S3 Frontend
  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "S3-Frontend"
    origin_access_control_id = aws_cloudfront_origin_access_control.s3_oac.id
  }

  # Origin 2: EC2 Backend
  origin {
    domain_name = aws_instance.studybot.public_dns
    origin_id   = "EC2-Backend"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only" # Traffic between CloudFront and EC2 is HTTP on port 80
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # Default Cache Behavior (serves S3 Frontend)
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-Frontend"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  # API Route Cache Behaviors (forwards backend requests directly to EC2)
  dynamic "ordered_cache_behavior" {
    for_each = ["/upload", "/query", "/summary", "/flashcards", "/quiz", "/docs/list", "/queries/recent", "/health"]
    content {
      path_pattern     = ordered_cache_behavior.value
      allowed_methods  = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
      cached_methods   = ["GET", "HEAD"]
      target_origin_id = "EC2-Backend"

      # Forward all query strings, headers (like X-User-Id), and cookies
      forwarded_values {
        query_string = true
        headers      = ["*"]
        cookies {
          forward = "all"
        }
      }

      # API responses must not be cached by CloudFront
      viewer_protocol_policy = "redirect-to-https"
      min_ttl                = 0
      default_ttl            = 0
      max_ttl                = 0
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
