# Phần 6: Cấu hình cài đặt chương trình quản lý khởi động hệ thống (Boot Manager) - Exam 101

Tài liệu này trình bày về trình quản lý khởi động GRUB (GRUB Stage 1, Legacy GRUB, GRUB2), so sánh MBR và GPT, và cách cấu hình, tương tác với GRUB/GRUB2 trên hệ điều hành Linux.

---

## 1. Trình quản lý khởi động GRUB & MBR

### Cơ chế Stage 1 của GRUB trong MBR:
- **MBR (Master Boot Record)** là cung mồi (sector) đầu tiên của ổ đĩa, có dung lượng cực kỳ giới hạn (chỉ **512 bytes**). Vì dung lượng quá nhỏ, MBR không thể chứa toàn bộ mã nguồn của một trình khởi động phức tạp như GRUB.
- Do đó, GRUB được chia làm các phân đoạn (Stages):
  - **GRUB Stage 1**: Được cài đặt trực tiếp vào phân vùng đặc biệt dài 512 bytes ở đầu ổ đĩa (MBR). Nó hoạt động như một "phái viên bắc cầu", nhiệm vụ duy nhất của nó là định vị và tải tiếp **Stage 1.5** hoặc **Stage 2** của GRUB (nằm ở các phân vùng khác trên ổ đĩa) để tiếp tục quá trình khởi động.

### Làm việc với Legacy GRUB Shell:
Để vào môi trường dòng lệnh của GRUB Legacy, sử dụng lệnh `grub`. Các câu lệnh cơ bản trong Grub Shell:
- **`grub`**: Lệnh truy cập vào môi trường Grub Shell để thực thi lệnh cứu hộ boot.
- **`help`**: Hiển thị danh sách câu lệnh hỗ trợ hoặc thông tin chi tiết một lệnh cụ thể.
- **`find <file>`**: Tìm kiếm sự tồn tại của một file cụ thể trên các phân vùng và trả về tên thiết bị ổ cứng (ví dụ: `find /boot/grub/stage1`).
- **`quit`**: Thoát khỏi môi trường Grub Shell.

---

## 2. So sánh chuẩn phân vùng MBR và GPT

Khi chuẩn bị phân vùng ổ đĩa, quản trị viên cần lựa chọn giữa hai định dạng bảng phân vùng:

| Đặc điểm | MBR (Master Boot Record) | GPT (GUID Partition Table) |
| :--- | :--- | :--- |
| **Kiểu thiết kế** | Chuẩn truyền thống cũ. | Chuẩn hiện đại mới. |
| **Số lượng phân vùng** | Hỗ trợ tối đa **26 phân vùng** (gồm 4 phân vùng chính Primary, và 23 phân vùng logic bên trong phân vùng mở rộng Extended). | Hỗ trợ lên đến **128 phân vùng** mà không cần cơ chế phân vùng mở rộng (Extended). |
| **Giới hạn dung lượng** | Chỉ hỗ trợ ổ cứng dưới **2 TB**. | Hỗ trợ ổ cứng dung lượng cực lớn lên đến **ZB** (Zettabyte - 1 ZB = 1 tỷ TB). |
| **Chuẩn Boot yêu cầu** | BIOS truyền thống (hoặc UEFI ở chế độ Legacy). | Cần chuẩn **UEFI** (Unified Extensible Firmware Interface). |
| **Tính năng an toàn** | Không có tính năng ngăn chặn hệ điều hành lạ. | Hỗ trợ **Secure Boot** giúp ngăn chặn các hệ điều hành/mã độc trái phép khởi động. |
| **Hỗ trợ hệ điều hành** | 32-bit và 64-bit. | Chỉ hỗ trợ hệ điều hành **64-bit**. |

---

## 3. Cấu hình và tương tác với GRUB / GRUB2

Hệ thống Linux hiện đại sử dụng GRUB2 với cơ chế cấu hình tự động thông qua các templates.

### Các file cấu hình GRUB quan trọng:
- **Legacy GRUB (GRUB cũ)**: `/boot/grub/grub.conf`
- **GRUB2**: 
  - Đường dẫn file cấu hình đã được biên dịch: `/boot/grub2/grub.cfg` (Trên hệ điều hành Debian/Ubuntu thường là `/boot/grub/grub.cfg`).
  - File cấu hình gốc dành cho quản trị viên chỉnh sửa: `/etc/default/grub`.

### Các câu lệnh quản lý GRUB2:
- **`grub2-editenv list`**: Liệt kê các tham số cấu hình môi trường khởi động mặc định (default boot entry) trong GRUB2.
- **`grub2-mkconfig`**: Tạo ra hoặc cập nhật file cấu hình `/boot/grub2/grub.cfg` dựa trên các thiết lập trong `/etc/default/grub`.
  *(Trên Debian/Ubuntu sử dụng lệnh `grub-mkconfig`)*
- **`update-grub`**: Lệnh viết tắt được sử dụng trên các hệ điều hành nhân Debian (như Ubuntu) để cập nhật nhanh cấu hình GRUB2 sau khi chỉnh sửa file `/etc/default/grub`.

### Tương tác trực tiếp trên Menu Legacy GRUB lúc khởi động:
- Phím **`[A]`**: Thêm tùy chọn/tham số khởi động vào cuối dòng kernel trước khi boot.
- Phím **`[C]`**: Truy cập vào chế độ dòng lệnh (GRUB Command Line Mode).
- Phím **`[ESC]`**: Thoát khỏi menu chỉnh sửa hoặc quay lại menu chính.
- **Các phím mũi tên**: Dùng để di chuyển lên/xuống để chọn hệ điều hành hoặc kernel muốn boot.
