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
# AMI Datasource for Amazon Linux 2023
# ---------------------------------------------------------
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# ---------------------------------------------------------
# Security Group for EC2
# ---------------------------------------------------------
resource "aws_security_group" "ec2" {
  name        = "${var.project}-ec2-sg"
  description = "Security group for StudyBot EC2 instance"
  vpc_id      = data.aws_vpc.default.id

  # Inbound HTTP (CloudFront will access our app on port 80)
  ingress {
    description = "Allow HTTP inbound from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound access to allow EC2 to connect to ECR, S3, DynamoDB, Bedrock
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ---------------------------------------------------------
# IAM Instance Profile (Attaches IAM Role to EC2)
# ---------------------------------------------------------
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project}-ec2-instance-profile"
  role = aws_iam_role.apprunner_instance_role.name
}

# ---------------------------------------------------------
# EC2 Instance (t3.micro - Free Tier)
# ---------------------------------------------------------
resource "aws_instance" "studybot" {
  ami                  = data.aws_ami.amazon_linux_2023.id
  instance_type        = "t3.micro"
  subnet_id            = element(data.aws_subnets.default.ids, 0)
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  vpc_security_group_ids = [aws_security_group.ec2.id]

  associate_public_ip_address = true

  # Startup script to configure Docker and pull/run ECR container
  user_data = <<-EOF
    #!/bin/bash
    # Update packages and install Docker
    dnf update -y
    dnf install -y docker
    systemctl start docker
    systemctl enable docker

    # Log in to ECR
    aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.studybot.repository_url}
    
    # Pull ECR image
    docker pull ${aws_ecr_repository.studybot.repository_url}:${var.ecr_image_tag}
    
    # Run container mapping standard port 80 to container port 8000
    docker run -d --name studybot -p 80:8000 \
      -e AI_BACKEND=bedrock \
      -e AI_MODEL_ID=${var.ai_model_id} \
      -e AWS_REGION=${var.aws_region} \
      -e STORAGE_BACKEND=s3 \
      -e STORAGE_BUCKET=${aws_s3_bucket.docs.id} \
      -e USERSTORE_BACKEND=dynamodb \
      -e USERSTORE_TABLE=${aws_dynamodb_table.users.name} \
      -e VECTOR_BACKEND=local \
      -e SERVE_FRONTEND=false \
      ${aws_ecr_repository.studybot.repository_url}:${var.ecr_image_tag}
  EOF

  tags = {
    Name = "${var.project}-backend"
  }
}
