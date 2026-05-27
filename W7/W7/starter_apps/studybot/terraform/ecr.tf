resource "aws_ecr_repository" "studybot" {
  name                 = var.project
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  force_delete = true # Allows clean teardown of the repository even if it contains images
}
