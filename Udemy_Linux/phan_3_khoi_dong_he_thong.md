# Phần 3: Khởi động Hệ thống Linux (Linux Boot System)

Tài liệu này tổng hợp kiến thức về quá trình khởi động hệ thống Linux, các mức chạy (Runlevel), sự chuyển dịch từ SysV init/Upstart sang Systemd, cách quản lý Unit Files của Systemd, và các câu lệnh kiểm tra thông điệp khởi động của kernel.

---

## 1. Kiểm tra Bộ đệm Vòng Nhân (Kernel Ring Buffer)

Khi hệ thống Linux khởi động, Kernel sẽ tải và cấu hình phần cứng, đồng thời xuất ra rất nhiều thông điệp log. Do lúc này các dịch vụ log của hệ thống (như syslog) chưa chạy, các thông điệp này được lưu trữ tạm thời trong **Kernel Ring Buffer**.

Để kiểm tra các thông báo này, ta sử dụng:
- **`dmesg`**: Lệnh truyền thống dùng để xem toàn bộ nội dung của bộ đệm vòng nhân (kernel ring buffer). Thường dùng để gỡ lỗi thiết bị phần cứng khi cắm vào hệ thống.
- **`journalctl -k`**: Lệnh của hệ thống `systemd` dùng để lọc và xem thông điệp từ bộ đệm vòng nhân được ghi nhận lại trong systemd journal (tương đương với `dmesg`).

---

## 2. Các Mức Chạy (Runlevels) trong Linux

Runlevel xác định trạng thái hoạt động của hệ thống và các dịch vụ nào sẽ được khởi động cùng hệ điều hành. Dưới đây là bảng phân loại các Runlevel tiêu chuẩn:

| Runlevel | Tên / Trạng thái | Mục đích |
| :---: | :--- | :--- |
| **0** | **Halt** | Tắt hoàn toàn hệ thống (Shutdown). |
| **1** | **Single-user mode** | Chế độ một người dùng. Không cấu hình mạng (networking), chỉ khởi động các tiến trình tối thiểu. Thường dùng cho việc bảo trì, sửa lỗi và khôi phục hệ thống dưới quyền root. |
| **2** | **Multi-user mode (no network)** | Chế độ đa người dùng nhưng không có kết nối mạng (no networking), khởi động các tiến trình cơ bản. |
| **3** | **Multi-user mode (CLI)** | Chế độ đa người dùng đầy đủ mạng (with networking). Hệ thống khởi động bình thường ở giao diện dòng lệnh (Command Line Interface - CLI). Đây là chế độ mặc định của hầu hết các máy chủ (servers). |
| **4** | **Unused** | Chưa được định nghĩa / Chưa sử dụng (người dùng tự tùy biến). |
| **5** | **Multi-user mode (GUI)** | Chế độ đa người dùng đầy đủ mạng (with networking) kết hợp giao diện đồ họa (Graphical User Interface - GUI). Đây là chế độ mặc định của các phiên bản Desktop. |
| **6** | **Reboot** | Khởi động lại hệ thống. |

---

## 3. Quá trình chuyển dịch sang Systemd

Hầu hết các bản phân phối Linux hiện đại đã chuyển từ hệ thống quản lý khởi động cũ (**SysV init** hoặc **Upstart**) sang **Systemd**.

### Tại sao lại chọn Systemd?
- **Tốc độ khởi động vượt trội:** 
  - Hệ thống cũ (Init/Upstart) phụ thuộc nhiều vào các **Shell Scripts (Bash)**. Việc chạy các shell script này làm chậm tốc độ khởi động dịch vụ và hệ điều hành do phải thực thi tuần tự.
  - **Systemd** thay thế hầu hết các tập lệnh Shell khởi động bằng mã nguồn **ngôn ngữ C** đã được biên dịch, giúp xử lý song song và tăng tốc độ khởi động vượt bậc.
- **Khả năng tương thích:**
  - Systemd vẫn hỗ trợ và tương thích ngược với các shell script của hệ điều hành Linux sử dụng SystemV init cũ.
  - *Ghi chú từ tác giả của Systemd:* Hệ thống không tương thích hoàn toàn 100% với cái cũ, nhưng độ tương thích đạt trên 99%.

---

## 4. Quản lý Unit Files trong Systemd

Trong Systemd, các dịch vụ, điểm mount, thiết bị... được quản lý dưới dạng các **Units** thông qua các **Unit Files**.

### Các vị trí lưu trữ Unit Files (Thứ tự ưu tiên)

1.  **`/lib/systemd/system`** hoặc **`/usr/lib/systemd/system`**
    - **Vị trí mặc định:** Được cung cấp bởi các gói phần mềm (packages) khi cài đặt.
    - *Lưu ý:* **Không tự ý soạn thảo hoặc chỉnh sửa** các file trong thư mục này vì chúng sẽ bị ghi đè khi cập nhật phần mềm.
2.  **`/etc/systemd/system`**
    - **Vị trí dành cho quản trị viên (System Administrator):** Đây là nơi chứa các unit files tự tạo hoặc cấu hình tùy biến của quản trị viên.
    - Thư mục này có **quyền ưu tiên cao nhất** và sẽ ghi đè (override) lên các file cấu hình cùng tên nằm trong thư mục `/usr`.
3.  **`/run/systemd/system`**
    - **Runtime unit files:** Lưu trữ các file cấu hình được tạo ra trong thời gian chạy (runtime) và sẽ mất đi khi khởi động lại hệ thống.

*   Để liệt kê tất cả các unit files hiện có trên hệ thống, sử dụng lệnh:
    ```bash
    systemctl list-unit-files
    ```

---

## 5. Cấu trúc và thành phần của một Unit File

Các Unit Files tuân theo định dạng cấu hình kiểu **INI** (tương tự như định dạng file cấu hình lần đầu xuất hiện trong MS-DOS), sử dụng các cặp `Key=Value` chia theo từng phân đoạn (sections).

### Ví dụ về cấu trúc một Unit File:
```ini
[Unit]
Description=Multi-User System
Documentation=man:system.special(7)
Requires=basic.target
Conflicts=rescue.service rescue.target
After=basic.target rescue.service rescue.target

[Service]
# Các cấu hình chạy dịch vụ nằm ở đây...
```

### Chi tiết các thuộc tính cơ bản trong phân đoạn `[Unit]`:
- **`Description=`**: Mô tả ngắn gọn về chức năng của Unit này.
- **`Documentation=`**: Đường dẫn đến tài liệu hướng dẫn (ví dụ: trang hướng dẫn man page).
- **`Requires=`**: Các unit phụ thuộc bắt buộc. Nếu unit này được kích hoạt, các unit trong danh sách `Requires` cũng sẽ được kích hoạt. Nếu các unit phụ thuộc lỗi, unit này sẽ không chạy được.
- **`Wants=`**: Tương tự như `Requires` nhưng an toàn và linh hoạt hơn (more robust). Nếu các unit phụ thuộc trong `Wants` bị lỗi hoặc không kích hoạt được, unit chính vẫn sẽ tiếp tục khởi chạy bình thường.
- **`Conflicts=`**: Danh sách các unit xung đột. Nếu bất kỳ unit nào trong danh sách này đang chạy, unit hiện tại sẽ không thể khởi động (hoặc sẽ tắt unit xung đột kia đi).
- **`After=`**: Quy định thứ tự khởi động. Chỉ ra rằng unit hiện tại chỉ được khởi chạy **sau khi** các unit được liệt kê ở đây đã khởi động xong (lưu ý: `After` không tạo ra quan hệ phụ thuộc như `Requires`/`Wants`, nó chỉ quy định thứ tự thời gian).

*   Để xem toàn bộ hướng dẫn cấu trúc Unit file chi tiết, bạn sử dụng lệnh:
    ```bash
    man 5 system.unit
    ```
