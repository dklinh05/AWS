variable "aws_region" {
  type        = string
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "project" {
  type        = string
  description = "Project name"
  default     = "studybot"
}

variable "team" {
  type        = string
  description = "Team name for tagging"
  default     = "G1"
}

variable "ai_model_id" {
  type        = string
  description = "Bedrock Claude Sonnet model ID or inference profile ID"
  default     = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
}

variable "ecr_image_tag" {
  type        = string
  description = "Tag of the Docker image to deploy"
  default     = "latest"
}
