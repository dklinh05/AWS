# 🚀 W7 StudyBot — Kế hoạch Deploy với Terraform

> **Mục tiêu:** Từ app đang chạy local → **public HTTPS URL trên AWS** trước thứ Sáu 30/5.  
> **Stack:** App Runner (compute) + DynamoDB + S3 + CloudFront + Bedrock + Terraform IaC  
> **Budget:** ~$5–10 / 48h (dưới $30 để qualify bonus)

---

## 📍 Hiện trạng (Done ✅)

- [x] App chạy local: Upload file → Quiz / Summary / Flashcard hoạt động
- [x] Kết nối Bedrock Claude Sonnet 4.5 thành công
- [x] Frontend: Quiz clickable, Flashcard lật được, nút active đúng
- [x] Auto re-index file khi restart server

---

## 🗺️ Kiến trúc Target

```
User Browser
     │
     ▼
[CloudFront] ──── S3 (frontend static HTML)
     │
     ▼
[App Runner] ─── FastAPI (studybot app)
     │
     ├──► [S3 Bucket] (uploaded documents)
     ├──► [DynamoDB] (user sessions, doc metadata)
     └──► [Bedrock] (Claude Sonnet 4.5 via inference profile)
```

**7 Mandatory Capabilities:**
| # | Capability | Service |
|---|-----------|---------|
| 1 | User-Facing Entry | CloudFront + S3 static |
| 2 | Application Compute | **App Runner** |
| 3 | AI Feature | Bedrock (Claude Sonnet 4.5) ✅ Done |
| 4 | Data Persistence | **DynamoDB** |
| 5 | Object Storage | **S3** |
| 6 | Network Foundation | VPC + Security Groups (App Runner managed) |
| 7 | IAM Least-Privilege | IAM Role cho App Runner |

---

## 📋 Kịch bản từng bước

---

### PHASE 0 — Chuẩn bị (30 phút)

#### Bước 0.1 — Pre-flight checklist
- [ ] MFA bật trên AWS root account
- [ ] Budget alert $80 tại AWS Budgets → tạo budget → SNS email → **confirm email**
- [ ] Cost Anomaly Detection bật
- [ ] Bedrock model access: Claude Sonnet 4.5 ✅ đã có
- [ ] Cài Terraform: `terraform -v` → nếu chưa có, tải tại https://developer.hashicorp.com/terraform/install

#### Bước 0.2 — Tạo ECR (nơi chứa Docker image)
```bash
# Tạo ECR repo (sẽ dùng trong bước build image)
aws ecr create-repository --repository-name studybot --region us-east-1
```

#### Bước 0.3 — Tạo file cấu trúc Terraform
```
studybot/
├── terraform/
│   ├── main.tf          # Provider, backend
│   ├── variables.tf     # Input variables
│   ├── iam.tf           # IAM roles & policies
│   ├── s3.tf            # S3 buckets (docs + frontend)
│   ├── dynamodb.tf      # DynamoDB table
│   ├── ecr.tf           # Container registry
│   ├── apprunner.tf     # App Runner service
│   ├── cloudfront.tf    # CDN + HTTPS
│   └── outputs.tf       # URLs sau deploy
└── Dockerfile           # Container build
```

---

### PHASE 1 — Đóng gói App thành Docker Image (45 phút)

#### Bước 1.1 — Tạo Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY frontend/ ./frontend/
EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Bước 1.2 — Build và push lên ECR
```bash
# Login ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t studybot .

# Tag & Push
docker tag studybot:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/studybot:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/studybot:latest
```

#### Bước 1.3 — Test image local
```bash
docker run -p 8000:8000 \
  -e AI_BACKEND=bedrock \
  -e AI_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0 \
  -e AWS_REGION=us-east-1 \
  -e AWS_ACCESS_KEY_ID=... \
  -e AWS_SECRET_ACCESS_KEY=... \
  studybot
```

---

### PHASE 2 — Viết Terraform (60 phút)

#### Bước 2.1 — `terraform/variables.tf`
```hcl
variable "aws_region"    { default = "us-east-1" }
variable "project"       { default = "studybot" }
variable "team"          { default = "G1" }
variable "ai_model_id"   { default = "us.anthropic.claude-sonnet-4-5-20250929-v1:0" }
variable "ecr_image_uri" { description = "ECR image URI after push" }
```

#### Bước 2.2 — `terraform/s3.tf` — S3 Buckets
- S3 cho file upload (block public access)
- S3 cho static frontend
- Versioning ON, tags W7Capstone

#### Bước 2.3 — `terraform/dynamodb.tf` — DynamoDB
- Table: `studybot-users`
- Billing: PAY_PER_REQUEST (on-demand, free tier friendly)
- Partition key: `user_id` (String)

#### Bước 2.4 — `terraform/iam.tf` — IAM Role cho App Runner
Permissions cần thiết (least-privilege):
```
bedrock:InvokeModel
bedrock:Converse
s3:GetObject, s3:PutObject, s3:ListBucket
dynamodb:GetItem, PutItem, UpdateItem, Query, Scan
```

#### Bước 2.5 — `terraform/apprunner.tf` — App Runner
- Source: ECR image
- CPU: 1 vCPU, Memory: 2 GB
- Port: 8000
- Environment variables: AI_MODEL_ID, STORAGE_BACKEND=s3, USERSTORE_BACKEND=dynamodb
- Auto scaling: min 1, max 3

#### Bước 2.6 — `terraform/cloudfront.tf` — CloudFront
- Origin 1: S3 bucket (frontend HTML)
- Origin 2: App Runner URL (API calls `/api/*`)
- HTTPS only (CloudFront cấp SSL tự động)
- Price class: PriceClass_100 (US + Europe, rẻ nhất)

#### Bước 2.7 — `terraform/outputs.tf`
```hcl
output "cloudfront_url" { value = aws_cloudfront_distribution.main.domain_name }
output "app_runner_url" { value = aws_apprunner_service.studybot.service_url }
output "s3_docs_bucket" { value = aws_s3_bucket.docs.bucket }
output "dynamodb_table" { value = aws_dynamodb_table.users.name }
```

---

### PHASE 3 — Cập nhật .env và code để dùng AWS (30 phút)

#### Bước 3.1 — Cập nhật `.env` cho production
```env
AI_BACKEND=bedrock
AI_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
AWS_REGION=us-east-1
STORAGE_BACKEND=s3
STORAGE_BUCKET=studybot-docs-<account_id>
USERSTORE_BACKEND=dynamodb
USERSTORE_TABLE=studybot-users
VECTOR_BACKEND=local
SERVE_FRONTEND=true
```

> ⚠️ Khi chạy trên App Runner, KHÔNG cần AWS_ACCESS_KEY_ID/SECRET — App Runner dùng IAM Role tự động.

#### Bước 3.2 — Upload frontend lên S3
```bash
aws s3 cp frontend/index.html s3://studybot-frontend-<id>/index.html \
  --content-type "text/html"
```

---

### PHASE 4 — Deploy (30 phút)

```bash
cd terraform/

# Khởi tạo Terraform
terraform init

# Xem plan trước
terraform plan -var="ecr_image_uri=<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/studybot:latest"

# Deploy
terraform apply -var="ecr_image_uri=..." -auto-approve

# Lấy URL
terraform output cloudfront_url
```

#### Bước 4.1 — Kiểm tra sau deploy
- [ ] Mở CloudFront URL trên browser → app loads
- [ ] Upload 1 file test → thấy trong danh sách docs
- [ ] Bấm Quiz → câu hỏi AI sinh ra thật
- [ ] Mở từ phone hotspot → vẫn hoạt động (khác network)

---

### PHASE 5 — Evidence Pack (45 phút)

Tạo file `docs/W7_evidence.md` với 8 sections:

```
docs/
├── W7_evidence.md          ← Evidence Pack (bắt buộc)
├── architecture.png        ← Diagram
├── slides.pdf              ← 12-18 slides
├── demo.mp4                ← Video 3 phút (bắt buộc!)
└── screenshots/
    ├── cost_day1_eod.png
    ├── cost_day2_eod.png
    ├── cost_friday.png
    ├── iam_role.png
    ├── s3_bucket.png
    └── dynamodb_table.png
```

#### Bước 5.1 — Tạo DECISION blocks (Section 6.5, bắt buộc)
Ví dụ:
```
DECISION: App Runner thay vì Lambda cho Application Compute

ALTERNATIVES CONSIDERED:
- Lambda — bị giới hạn 15 phút timeout, cold start latency khi upload PDF lớn
- ECS Fargate — phức tạp hơn, cần cấu hình cluster/task definition, overkill cho hackathon

MEASUREMENT:
- App Runner deploy time: ~3 phút vs ECS ~15 phút
- App Runner minimum cost: $0.064/vCPU-hr vs ECS: $0.04/vCPU-hr (chấp nhận được)

TRADE-OFF ACCEPTED:
- App Runner đắt hơn ECS ~60% về compute cost nhưng tiết kiệm ~4-5h setup time
```

---

### PHASE 6 — Demo Prep (30 phút)

#### Bước 6.1 — Demo script (3 phút)
1. (30s) Giới thiệu: "StudyBot — AI Study Buddy, upload lecture → quiz/flashcard/summary"
2. (30s) Upload file PDF/TXT
3. (45s) Bấm Flashcard → lật thẻ
4. (45s) Bấm Quiz → chọn đáp án → xem giải thích
5. (30s) Bấm Tóm tắt → đọc summary

#### Bước 6.2 — Record video (Loom / OBS)
- Record đúng script trên
- Upload vào repo: `docs/demo.mp4`

---

## 💰 Ước tính chi phí (48h)

| Service | Cost |
|---------|------|
| App Runner (1 vCPU, 2GB) | ~$2.88 |
| S3 storage + requests | ~$0.05 |
| DynamoDB on-demand | ~$0.01 |
| CloudFront (1GB) | ~$0.09 |
| Bedrock (Claude Sonnet 4.5) | ~$1.00–2.00 |
| **TOTAL** | **~$4–6** |

✅ Dưới $30 → qualify bonus cost discipline

---

## ⚠️ Lưu ý quan trọng

1. **Không dùng NAT Gateway** — App Runner access Bedrock/S3/DynamoDB qua internet endpoint hoặc VPC endpoint
2. **Tag mọi resource:** `Project=W7Capstone`, `Team=G<N>`, `Owner=<name>`, `Environment=hackathon`
3. **Teardown bắt buộc** trước 23:59 Chủ nhật 1/6:
   ```bash
   terraform destroy -auto-approve
   ```
4. **Screenshot Cost Explorer** thứ Hai 2/6 → commit `docs/teardown_confirmed.png`

---

## 📅 Timeline gợi ý

| Thời gian | Việc làm |
|-----------|----------|
| **Bây giờ** | Phase 0: Pre-flight + cài Terraform |
| **Tối nay** | Phase 1: Dockerfile + push ECR |
| **Sáng thứ 4 (28/5)** | Phase 2: Viết Terraform code |
| **Chiều thứ 4** | Phase 3+4: Deploy lên AWS, test happy path |
| **Sáng thứ 5 (29/5)** | Phase 5: Evidence Pack |
| **Chiều thứ 5** | Phase 6: Demo video + slides |
| **Tối thứ 5** | Final test từ phone hotspot |
| **Sáng thứ 6 (30/5)** | Warm-up query lúc 8:45, demo |


<!-- Amazon App Runner (Compute):

Chạy Docker Container chứa mã nguồn backend FastAPI.
Tự động scale, hỗ trợ HTTPS sẵn có mà không cần tạo ALB hay NAT Gateway phức tạp, giúp tối ưu hóa chi phí (~$2–3/48h).
Amazon S3 (Object Storage):

S3 Bucket 1 (tài liệu): Lưu trữ các tài liệu PDF/TXT được upload lên (cấu hình block public access).
S3 Bucket 2 (frontend): Lưu trữ và host các file HTML tĩnh của giao diện web.
Amazon DynamoDB (Database):

Cơ sở dữ liệu NoSQL lưu trữ lịch sử hội thoại, danh sách file đã upload của user.
Sử dụng chế độ thanh toán theo lượt truy vấn (PAY_PER_REQUEST) để tiết kiệm tối đa chi phí.
Amazon Bedrock (AI/LLM):

Cung cấp mô hình Claude Sonnet 4.5 (us.anthropic.claude-sonnet-4-5-20250929-v1:0) xử lý các yêu cầu tạo Quiz, Summary, Flashcard.
Amazon CloudFront (CDN/Routing):

Điểm truy cập HTTPS duy nhất (Public URL) cho toàn bộ ứng dụng.
Định tuyến (routing):
Các request /api/* sẽ được chuyển hướng tới App Runner backend.
Các request giao diện còn lại sẽ trỏ trực tiếp tới S3 static frontend.
Amazon ECR (Container Registry):

Lưu trữ Docker image của StudyBot sau khi được build từ local. App Runner sẽ kéo image này về để deploy.
AWS IAM (Security & Permissions):

Thiết lập IAM Instance Role cấp quyền tối thiểu (least-privilege) để App Runner truy cập trực tiếp vào S3, DynamoDB và Bedrock mà không cần lưu Access Key/Secret Key trong code. -->
