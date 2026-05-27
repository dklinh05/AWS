resource "aws_dynamodb_table" "users" {
  name         = "${var.project}-users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"
  range_key    = "sk"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  # Ensure clean deletion and billing compliance
  point_in_time_recovery {
    enabled = false
  }
}
