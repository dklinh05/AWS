# BYOL Spring Boot trên Lambda - Ghi chú

## Q4.1: Lựa chọn Chiến lược (Which strategy did you pick?)

Tôi chọn **Chiến lược A (Strategy A): `aws-serverless-java-container-springboot3`**.

## Q4.6: Giải thích lý do (Why did you pick this option?)

Dựa trên các hướng tiếp cận được đề xuất trong `README.md`, tôi quyết định chọn Chiến lược A với các lý do sau:

1. **Giải pháp chuẩn (Canonical Answer):** Đây là phương pháp phổ biến, chuẩn mực và được hỗ trợ tốt nhất khi muốn đưa một ứng dụng Spring Boot truyền thống lên AWS Lambda.
2. **Hạn chế thay đổi mã nguồn cốt lõi (Low Code-Change Cost):**
   - Chúng ta chỉ cần thêm một class adapter mới (`StreamLambdaHandler`) và cập nhật cấu hình Maven (`pom.xml` với `maven-shade-plugin`).
   - Mã nguồn ứng dụng (như các class `@RestController` hay `@SpringBootApplication`) hoàn toàn **không cần thay đổi** và không bị dính chặt (couple) vào bất kỳ thư viện nào của Lambda. Ứng dụng vẫn giữ được tính độc lập của framework.
3. **Phát triển cục bộ (Local Development) dễ dàng:** Do không sửa đổi code controller, việc chạy ứng dụng ở máy local (ví dụ: `mvn spring-boot:run` trên Tomcat) vẫn giữ nguyên trải nghiệm và sự tiện lợi vốn có của Spring Boot.
4. **Hiệu suất và Tối ưu hóa:** Mặc dù Chiến lược B (Web Adapter) yêu cầu ít cấu hình hơn, Chiến lược A cung cấp sự tích hợp sâu và nguyên bản (native) hơn, giúp tránh được độ trễ do phải chạy qua một proxy HTTP trung gian.
5. **Sẵn sàng cho SnapStart:** Dù Java có thời gian "cold start" (khởi động lạnh) tương đối cao (5-10 giây), Chiến lược A là bước đệm hoàn hảo để tích hợp tính năng **AWS Lambda SnapStart** (như đề cập ở phần Bonus B). SnapStart có thể giảm thời gian cold start xuống mức cực kì ấn tượng (chỉ còn 200-500 ms), giải quyết nút thắt cổ chai về hiệu năng lớn nhất của Java trên Lambda và biến đây thành một lựa chọn thực tế, tối ưu cho môi trường Production.

![alt text](image.png)
