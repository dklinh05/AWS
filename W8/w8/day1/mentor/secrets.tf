# Create a Secrets Manager secret metadata container

resource "aws_secretsmanager_secret" "app_secret" {
  name                    = "${local.name_prefix}-app-db-secret"
  description             = "Database credentials for the application"
  recovery_window_in_days = 0 # Setting to 0 for immediate deletion in training/dev environments

  tags = local.common_tags
}

# Create a Secret Version storing the actual sensitive values.
# The sensitive variable `var.db_password` is formatted as JSON and injected.
# In the CLI, this value will be masked as `(sensitive value)` and won't leak in logs.
resource "aws_secretsmanager_secret_version" "app_secret_val" {
  secret_id = aws_secretsmanager_secret.app_secret.id
  secret_string = jsonencode({
    db_username = "mentor_admin"
    db_password = var.db_password
  })
}
