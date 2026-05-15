# Ghi chú Lựa chọn Chiến lược (Strategy) - Go Gin

## Q4.1: Bạn đã chọn chiến lược nào? (Which strategy did you pick?)
Tôi chọn **Chiến lược A (Strategy A): `aws-lambda-go-api-proxy/gin`**.

## Q4.6: Tại sao bạn lại chọn lựa chọn này? (Why did you pick this option?)
Dựa trên các hướng tiếp cận trong `README.md`, tôi chọn Chiến lược A vì những lý do sau:

1. **Hiệu năng cực tốt (Excellent Performance):** Go vốn đã rất nhanh, và với adapter chuyên dụng này, thời gian khởi động lạnh (cold start) chỉ mất khoảng **50–150 ms**. Đây là con số ấn tượng so với các runtime khác.
2. **Chi phí thay đổi thấp (Low Code-Change Cost):** 
   - Chỉ cần thêm khoảng 8 dòng code để tạo file `main.go` ở thư mục gốc làm entrypoint cho Lambda.
   - Không cần thay đổi bất kỳ logic nào trong router Gin hiện có ở `server/server.go`. Điều này tuân thủ đúng nguyên tắc "giữ cho framework layer sạch sẽ".
3. **Độ tin cậy cao:** Thư viện `aws-lambda-go-api-proxy` được duy trì bởi AWS Labs, đảm bảo việc ánh xạ giữa API Gateway và Gin router diễn ra mượt mà và chính xác.
4. **Hỗ trợ Full-Featured:** Khác với việc tự viết router thủ công (Chiến lược C), adapter này hỗ trợ đầy đủ các tính năng của Gin mà không tốn nhiều công sức triển khai lại.

## Ghi chú triển khai (Deployment Notes)
- Tên stack khi đẩy lên AWS đã được đổi thành: **`linh-byol-go-gin`** (đảm bảo prefix `linh-` và vẫn giữ `byol-` như yêu cầu).
- Region mặc định: `us-west-2`.
