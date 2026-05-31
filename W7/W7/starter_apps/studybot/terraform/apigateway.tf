# ---------------------------------------------------------
# API Gateway HTTP API
# ---------------------------------------------------------
resource "aws_apigatewayv2_api" "api" {
  name          = "${var.project}-http-api"
  protocol_type = "HTTP"
}

# ---------------------------------------------------------
# Integration with Lambda Function
# ---------------------------------------------------------
resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"

  connection_type        = "INTERNET"
  description            = "FastAPI lambda integration"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.studybot.arn
  payload_format_version = "2.0" # Required for HTTP API proxy
}

# ---------------------------------------------------------
# Routes (Forward everything to the Lambda proxy)
# ---------------------------------------------------------
resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# ---------------------------------------------------------
# Deployment Stage ($default)
# ---------------------------------------------------------
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

# ---------------------------------------------------------
# Permission for API Gateway to Invoke Lambda
# ---------------------------------------------------------
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.studybot.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}
