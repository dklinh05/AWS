# ---------------------------------------------------------
# App Runner ECR Access Role (Build/Deploy Role)
# ---------------------------------------------------------
data "aws_iam_policy_document" "apprunner_build_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "apprunner_access_role" {
  name               = "${var.project}-apprunner-access-role"
  assume_role_policy = data.aws_iam_policy_document.apprunner_build_trust.json
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# ---------------------------------------------------------
# App Runner Task Instance Role (Runtime Permissions Role)
# ---------------------------------------------------------
data "aws_iam_policy_document" "apprunner_tasks_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "apprunner_instance_role" {
  name               = "${var.project}-apprunner-instance-role"
  assume_role_policy = data.aws_iam_policy_document.apprunner_tasks_trust.json
}

# Least-privilege permissions for DynamoDB, S3 documents, and Bedrock AI
data "aws_iam_policy_document" "apprunner_permissions" {
  statement {
    sid       = "BedrockModelAccess"
    effect    = "Allow"
    actions   = [
      "bedrock:InvokeModel",
      "bedrock:Converse",
      "bedrock:ConverseStream",
      "bedrock:Retrieve",
      "bedrock:RetrieveAndGenerate",
      "bedrock:StartIngestionJob",
      "bedrock:GetIngestionJob",
      "bedrock:ListIngestionJobs",
      "bedrock:ListDataSources"
    ]
    resources = ["*"]
  }

  statement {
    sid       = "S3DocumentStorageAccess"
    effect    = "Allow"
    actions   = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
      "s3:DeleteObject"
    ]
    resources = [
      aws_s3_bucket.docs.arn,
      "${aws_s3_bucket.docs.arn}/*"
    ]
  }

  statement {
    sid       = "DynamoDBUserStoreAccess"
    effect    = "Allow"
    actions   = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
    resources = [
      aws_dynamodb_table.users.arn,
      "${aws_dynamodb_table.users.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "apprunner_permissions" {
  name   = "${var.project}-apprunner-permissions"
  role   = aws_iam_role.apprunner_instance_role.id
  policy = data.aws_iam_policy_document.apprunner_permissions.json
}

resource "aws_iam_role_policy_attachment" "ec2_ecr_readonly" {
  role       = aws_iam_role.apprunner_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.apprunner_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
