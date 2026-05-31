# ---------------------------------------------------------
# AWS Lambda Function (FastAPI Container)
# ---------------------------------------------------------
resource "aws_lambda_function" "studybot" {
  function_name = var.project
  role          = aws_iam_role.apprunner_instance_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.studybot.repository_url}:${var.ecr_image_tag}"
  timeout       = 30
  memory_size   = 1024

  environment {
    variables = {
      AI_BACKEND        = "bedrock"
      AI_MODEL_ID       = var.ai_model_id
      STORAGE_BACKEND   = "s3"
      STORAGE_BUCKET    = aws_s3_bucket.docs.id
      USERSTORE_BACKEND = "dynamodb"
      USERSTORE_TABLE   = aws_dynamodb_table.users.name
      VECTOR_BACKEND       = "bedrock_kb"
      VECTOR_BEDROCK_KB_ID = aws_bedrockagent_knowledge_base.studybot.id
      SERVE_FRONTEND       = "false"
      PORT                 = "8000" # Tells Lambda Web Adapter to forward requests to uvicorn on port 8000
    }
  }

  vpc_config {
    subnet_ids         = data.aws_subnets.default.ids
    security_group_ids = [aws_security_group.vpc_endpoints.id]
  }

  depends_on = [
    aws_iam_role_policy.apprunner_permissions,
    aws_iam_role_policy_attachment.ec2_ecr_readonly
  ]
}
