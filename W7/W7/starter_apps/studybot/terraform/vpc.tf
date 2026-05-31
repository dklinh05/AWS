# ---------------------------------------------------------
# Default VPC and Subnets Datasources
# ---------------------------------------------------------
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ---------------------------------------------------------
# Security Group for VPC Resources (Lambda & Endpoints)
# ---------------------------------------------------------
resource "aws_security_group" "vpc_endpoints" {
  name        = "${var.project}-endpoints-sg"
  description = "Security group for Lambda and Bedrock VPC endpoint communication"
  vpc_id      = data.aws_vpc.default.id

  # Allow all internal traffic within the VPC
  ingress {
    description = "Allow internal VPC traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ---------------------------------------------------------
# VPC Interface Endpoint for Bedrock Runtime
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "bedrock_runtime" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${var.aws_region}.bedrock-runtime"
  vpc_endpoint_type   = "Interface"
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  subnet_ids          = data.aws_subnets.default.ids
  private_dns_enabled = true
}

# ---------------------------------------------------------
# Route Tables Datasource (needed for Gateway Endpoints)
# ---------------------------------------------------------
data "aws_route_tables" "default" {
  vpc_id = data.aws_vpc.default.id
}

# ---------------------------------------------------------
# VPC Gateway Endpoint for S3 (Free)
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = data.aws_route_tables.default.ids
}

# ---------------------------------------------------------
# VPC Gateway Endpoint for DynamoDB (Free)
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${var.aws_region}.dynamodb"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = data.aws_route_tables.default.ids
}

# ---------------------------------------------------------
# VPC Interface Endpoint for Bedrock Agent
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "bedrock_agent" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${var.aws_region}.bedrock-agent"
  vpc_endpoint_type   = "Interface"
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  subnet_ids          = data.aws_subnets.default.ids
  private_dns_enabled = true
}

# ---------------------------------------------------------
# VPC Interface Endpoint for Bedrock Agent Runtime
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "bedrock_agent_runtime" {
  vpc_id              = data.aws_vpc.default.id
  service_name        = "com.amazonaws.${var.aws_region}.bedrock-agent-runtime"
  vpc_endpoint_type   = "Interface"
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  subnet_ids          = data.aws_subnets.default.ids
  private_dns_enabled = true
}
