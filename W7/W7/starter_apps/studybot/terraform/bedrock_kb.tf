data "aws_caller_identity" "current" {}

# ---------------------------------------------------------
# S3 Vectors Resources (requires AWS Provider >= 6.27.0)
# ---------------------------------------------------------
resource "aws_s3vectors_vector_bucket" "studybot" {
  vector_bucket_name = "studybot-vectors-${random_string.suffix.result}"
}

resource "aws_s3vectors_index" "studybot" {
  index_name         = "studybot-index"
  vector_bucket_name = aws_s3vectors_vector_bucket.studybot.vector_bucket_name
  data_type          = "float32"
  dimension          = 1024
  distance_metric    = "cosine"
}

# ---------------------------------------------------------
# IAM Role for Bedrock Knowledge Base
# ---------------------------------------------------------
data "aws_iam_policy_document" "bedrock_kb_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "bedrock_kb_role" {
  name               = "${var.project}-bedrock-kb-role"
  assume_role_policy = data.aws_iam_policy_document.bedrock_kb_trust.json
}

data "aws_iam_policy_document" "bedrock_kb_permissions" {
  statement {
    sid       = "BedrockModelAccess"
    effect    = "Allow"
    actions   = ["bedrock:InvokeModel"]
    resources = [
      "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-embed-text-v2:0"
    ]
  }

  statement {
    sid       = "S3DocumentAccess"
    effect    = "Allow"
    actions   = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.docs.arn,
      "${aws_s3_bucket.docs.arn}/*"
    ]
  }

  statement {
    sid       = "S3VectorsAccess"
    effect    = "Allow"
    actions   = [
      "s3vectors:*"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "bedrock_kb_policy" {
  name   = "${var.project}-bedrock-kb-policy"
  role   = aws_iam_role.bedrock_kb_role.id
  policy = data.aws_iam_policy_document.bedrock_kb_permissions.json
}

# ---------------------------------------------------------
# Bedrock Knowledge Base
# ---------------------------------------------------------
resource "aws_bedrockagent_knowledge_base" "studybot" {
  name     = "${var.project}-kb"
  role_arn = aws_iam_role.bedrock_kb_role.arn

  knowledge_base_configuration {
    type = "VECTOR"
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-embed-text-v2:0"
    }
  }

  storage_configuration {
    type = "S3_VECTORS"
    s3_vectors_configuration {
      index_arn = aws_s3vectors_index.studybot.index_arn
    }
  }

  depends_on = [
    aws_iam_role_policy.bedrock_kb_policy
  ]
}

# ---------------------------------------------------------
# Bedrock Data Source (Linked to raw documents S3 bucket)
# ---------------------------------------------------------
resource "aws_bedrockagent_data_source" "studybot_docs" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.studybot.id
  name              = "${var.project}-docs-ds"

  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = aws_s3_bucket.docs.arn
    }
  }
}
