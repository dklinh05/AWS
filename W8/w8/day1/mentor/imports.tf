# File này dùng để minh họa tính năng HCL-native Import (Terraform 1.5+)
# Để tránh lỗi khi chạy `terraform plan` khi chưa có tài nguyên thật trên AWS, các khối bên dưới được comment lại.

# 1. Khai báo import block để trỏ tới tài nguyên thực tế
import {
  to = aws_s3_bucket.imported_bucket
  id = "mentor-training-dev-primary-bucket"
}

# 2. Bạn cần khai báo block resource tương ứng để Terraform import vào.
#chỉ cần chạy lệnh: terraform plan -generate-config-out=generated.tf
#resource "aws_s3_bucket" "imported_bucket" {
 # bucket        = "mentor-training-dev-primary-bucket"
#  force_destroy = true
#}

